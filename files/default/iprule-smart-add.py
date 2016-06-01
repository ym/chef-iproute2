#!/usr/bin/env python
from pyroute2 import IPRoute
from pyroute2.netlink.rtnl.fibmsg import FR_ACT_NAMES
from netaddr import IPNetwork
from socket import AF_INET
import click

ipr = IPRoute()

FR_ACT_NAMES_MAP = dict((v, k) for k, v in FR_ACT_NAMES.iteritems())
IPRULES_MAP = {
    'family': 'family',
    'action': FR_ACT_NAMES_MAP,
    'dst_len': 'dst_len',
    'src_len': 'src_len',
}
IPRULE_ATTRS_MAP = {
    'priority': 'FRA_PRIORITY',
    'table': 'FRA_TABLE',
    'src': 'FRA_SRC',
    'dst': 'FRA_DST',
}


def nla_slots_to_dict(slots):
    return {slot[0]: slot[1] for slot in slots}


def map_dict(d, mappings):
    ret = dict()
    for k, mapping in mappings.iteritems():
        map_type = type(mapping)
        if map_type == str:
            if mapping in d:
                ret[k] = d[mapping]
        elif map_type == dict:
            if k not in d:
                continue
            src = d[k]
            if src in mapping:
                ret[k] = mapping[src]
        else:
            continue
    return ret


def rule_to_dict(rule):
    attrs = nla_slots_to_dict(rule['attrs'])

    ret = map_dict(rule, IPRULES_MAP)
    ret.update(map_dict(attrs, IPRULE_ATTRS_MAP))

    return ret


def add_rule(from_cidr, table):
    cidr = IPNetwork(from_cidr).cidr
    table = int(table)

    hit = 0

    # Search existing rules
    for rule in ipr.get_rules(family=AF_INET):
        rule = rule_to_dict(rule)
        if not all(k in rule for k in ('src', 'src_len', 'table')):
            continue

        _cidr = IPNetwork("%s/%s" % (rule['src'], rule['src_len']))
        if _cidr != cidr or rule['table'] != table:
            continue

        hit += 1

        # Clean up existing malformed or duplicated rule
        if str(_cidr) != str(cidr) or hit > 1:
            ipr.rule('delete', **rule)
            hit -= 1

    if hit == 0:
        ipr.rule(
            'add', action='FR_ACT_TO_TBL',
            src=str(cidr.ip), src_len=cidr.prefixlen,
            table=table, family=AF_INET
        )


@click.command()
@click.argument('src')
@click.argument('table')
def add_rule_command(src, table):
    return add_rule(src, table)


if __name__ == '__main__':
    add_rule_command()
