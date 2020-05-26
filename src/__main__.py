from src.processor import Processor
from os import system, name
from time import sleep


def clear():
    # windows
    if name == 'nt':
        _ = system('cls')
    # linux mac
    else:
        _ = system('clear')


def execute_and_print(processor: Processor):
    c = processor.clock_update()
    clear()
    print(f"END OF CLOCK CYCLE {processor.clock_time}", end=' ')
    print("RESULTS")
    processor.first_stage.print_info_to_console()
    processor.second_stage.print_to_console()
    processor.third_stage.print_to_console()
    processor.fourth_stage.print_to_console()
    processor.fifth_stage.print_to_console()
    return c


if __name__ == '__main__':
    print("*****************WELCOME TO THE MIPS PROCESSOR*****************************")
    var = input("ENTER X to EXIT, OR PRESS ENTER TO CONTINUE: ")
    while var != 'x' and var != 'X':
        main_processor = Processor()
        clear()
        file_found = False
        var3 = 'w'
        while not file_found and var3 != 'x' and var3 != 'X':
            file_found = True
            print("TIP: ENTER PATHS RELATIVE TO src, OTHERWISE ENTER FULL PATH")
            file_path = input("Please Enter asm file: ")
            try:
                main_processor.load_file_into_im(file_path)
            except FileNotFoundError:
                file_found = False
                clear()
                var3 = input("FILE NOT FOUND:\nPRESS X TO EXIT OR PRESS ENTER TO RETRY ENTERING FILE PATH: ")
                clear()

        if not file_found:
            break
        print("FILE FOUND")
        sleep(1)
        clear()

        mode_prompt = '''Please Enter Mode number: '''
        print("DEFAULT MODES:")
        print("1 is default mode and it prints end state of asm file(no pipeline).")
        print("22 is pipeline mode and it prints end of state of asm file.")
        print("DEBUG MODES:")
        print("0 is debug mode and it goes instruction by instruction(no pipeline).")
        print("11 is pipeline mode and it goes through cycles.")

        print("any other key will result in <1> mode")
        try:
            mode = int(input(mode_prompt))
        except ValueError:
            mode = 1
        if mode != 0 and mode != 11:
            main_processor.mode = mode
            print("DEFAULT MODE SELECTED")
            print('Starting..........')
            sleep(1)
            clear()
            execute_and_print(main_processor)
        else:
            main_processor.mode = mode
            print("DEBUG MODE SELECTED")
            print('Starting..........')
            sleep(1)
            var2 = 'w'
            code = 1
            while code == 1 and var2 != 'x' and var2 != 'X':
                clear()
                execute_and_print(main_processor)
                code = main_processor.code
                var2 = input("PRESS X TO EXIT DEBUG MODE OR PRESS ENTER TO CONTINUE: ")

        main_processor.clean()
        var = str(input("END REACHED: ENTER X to EXIT, OR PRESS ENTER TO START OVER: "))

    Processor.clean(Processor())
    Processor.delete_index()
    clear()
    exit()
