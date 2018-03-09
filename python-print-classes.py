def print_classes(mod):
    for name, obj in inspect.getmembers(mod):
        if inspect.isclass(obj):
            print obj

