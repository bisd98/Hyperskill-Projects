command = ""
final_text = ""
formatters = ['plain',  'bold', 'italic', 'header', 'link',
              'inline-code', 'ordered-list', 'unordered-list',
              'new-line', 'ordered-list', 'unordered-list']
while command != "!done":
    command = input("Choose a formatter:")
    if command in formatters:
        if command == 'plain':
            final_text = final_text + input("Text: ")
        elif command == 'bold':
            final_text = final_text + '**' + input("Text: ") + '**'
        elif command == 'italic':
            final_text = final_text + '*' + input("Text: ") + '*'
        elif command == 'inline-code':
            final_text = final_text + '`' + input("Text: ") + '`'
        elif command == 'link':
            final_text = final_text + '[' + input("Label: ") + ']' + '(' + input("URL: ") + ')'
        elif command == 'header':
            level = int(input("Level: "))
            while not 1 <= level <= 6:
                print("The level should be within the range of 1 to 6")
                level = int(input("Level: "))
            final_text = final_text + '#' * level + ' ' + input("Text: ") + '\n'
        elif command == 'ordered-list':
            number = int(input("Number of rows: "))
            while not 0 < number:
                print("The number of rows should be greater than zero")
                number = int(input("Number of rows: "))
            for x in range(number):
                final_text = final_text + str(x + 1) + '. ' + input(f'Row #{x + 1}:') + '\n'
        elif command == 'unordered-list':
            number = int(input("Number of rows: "))
            while not 0 < number:
                print("The number of rows should be greater than zero")
                number = int(input("Number of rows: "))
            for x in range(number):
                final_text = final_text + '* ' + input(f'Row #{x + 1}:') + '\n'
        elif command == 'new-line':
            final_text = final_text + '\n'
        print(final_text)
    elif command == '!help':
        print('Available formatters:', *formatters, '\n',
              'Special commands: !help !done')
    elif command == '!done':
        pass
    else:
        print('Unknown formatting type or command')
result = open('output.md', 'w')
result.write(final_text)
result.close()
