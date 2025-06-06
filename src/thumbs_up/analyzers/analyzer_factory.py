import idaapi

analyzers_factory = {}      # Mapping from CPU name (according to IDA) to the init function

def createAnalyzer(logger, is_elf):
    """Create a CPU-based analyzer to be used by the program.

    Args:
        logger (logger): logger instance
        is_elf (bool): True iff analysing an ELF file

    Return Value:
        Created analyzer instance (None if CPU isn't supported yet)
    """
    # Code taken from:
    # https://reverseengineering.stackexchange.com/questions/11396/how-to-get-the-cpu-architecture-via-idapython
    # Kudos to tmr232
    try:
        info = idaapi.get_inf_structure()
        if info.is_64bit():
            bits = 64
        elif info.is_32bit():
            bits = 32
        # quite rare
        else:
            bits = 16
            
        # Check if we support this CPU
        proc_name = info.procName
        # Can now create the analyzer instance
    except:
        import ida_ida
        if ida_ida.inf_is_32bit_or_higher():
            if ida_ida.inf_is_32bit_exactly():
                bits = 32
            else:
                bits = 64
        else:
            bits = 16
        proc_name = ida_ida.inf_get_procname()
    # At the moment we don't care about the processors endianness.
    logger.info(f"Processor: {proc_name}, {bits}bit")
    if proc_name not in analyzers_factory:
        logger.error(f"Processor {proc_name} is NOT supported yet :(")
        return None
    return analyzers_factory[proc_name](logger, bits, is_elf)

def registerAnalyzer(cpu, init_fn):
    """Register the analyzer in the overall factory.

    Args:
        cpu (str): name of the CPU (using IDA's conventions)
        init_fn (function): init function for the class instance
    """
    global analyzers_factory

    analyzers_factory[cpu] = init_fn
