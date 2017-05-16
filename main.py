import argparse
import repo, server

def h_serve(args):
	s = server.RepoServer(repo.Repo(), keyfile=args.key, certfile=args.cert)
	s.thread.join()

def h_update(args):
	r = repo.Repo()
	r.update()

if __name__ == '__main__':
	subcmds = {
		'serve'  : h_serve,
		'update' : h_update,
	}

	# Setup argument parsing
	parser = argparse.ArgumentParser(description='Repository server for halibot')

	sub = parser.add_subparsers(title='commands', dest='cmd', metavar='COMMAND')

	serve = sub.add_parser('serve', help='run the server')
	serve.add_argument('-k', '--key',  help='SSL/TLS private key file to use')
	serve.add_argument('-c', '--cert', help='SSL/TLS certificate to use')
	update = sub.add_parser('update', help='update the repository\'s packages from their sources')

	args = parser.parse_args()

	# Try to run a subcommand
	if args.cmd != None:
		subcmds[args.cmd](args)
	else:
		parser.print_help()
