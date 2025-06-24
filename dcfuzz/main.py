

logger = logging.getLogger('dcfuzz.main')


TARGET: str
FUZZERS: Fuzzers = []
ARGS: cli.ArgsParser






def main():
    global ARGS, FUZZERS, TARGET

    ARGS = cli.ArgsParser().parse_args()
    TARGET = ARGS.target

    unsupported_fuzzers = config['target'][TARGET].get('unsupported',[])
    available_fuzzers = list(config['fuzzer'].keys())

    available_fuzzers = [ 
        fuzzer for fuzzer in available_fuzzers
        if fuzzer not in unsupported_fuzzers
    ]

    FUZZERS = availabe_fuzzers if 'all' in ARGS.fuzzer else ARGS.fuzzer


    for fuzzer in FUZZERS:
        if not fuzzing.check(TARGET, fuzer, OUTPUT):
            exit(1)

    try:








if __name__ == '__main__':
    main()
