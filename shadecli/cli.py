import argparse
import sys
import numpy as np

from shadecli import Shadecli

def run_cli():
	parser = argparse.ArgumentParser(prog='shadecli')
	parser.add_argument('--dry', action='store_true', help='dry help')
	subparsers = parser.add_subparsers(help='sub-command help')

	set_parser = subparsers.add_parser('set', help='set {shades} {value}')
	set_parser.add_argument('shade_spec', nargs=1)
	set_parser.add_argument('value', nargs='?', type=int, default=100)
	set_parser.set_defaults(func=do_set)

	sine_parser = subparsers.add_parser('sine', help='sine {phase}')
	sine_parser.add_argument('phase', nargs='?', type=int, default=0)
	sine_parser.set_defaults(func=do_sine)

	anim_parser = subparsers.add_parser('anim', help='anim')
	anim_parser.add_argument('speed', nargs='?', type=int, default=0)
	anim_parser.set_defaults(func=do_anim)

	p = parser.parse_args()
	p.func(p)

def do_set(args):
	Shadecli(args.dry).set_const(args.shade_spec, args.value)

def do_sine(args):
	Shadecli(args.dry).sine(args.phase)

def do_anim(args):
	Shadecli(args.dry).anim(args.speed)
