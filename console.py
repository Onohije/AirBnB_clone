#!/usr/bin/env python3
"""The entry point of the command interprerter"""


import cmd
import re
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.file_storage import FileStorage


class HBNBCommand(cmd.Cmd):
    """Creating the command interpreter class"""
    prompt = "(hbnb) "
    valid_classes = ['BaseModel', 'User', 'State', 'City',
                     'Amenity', 'Place', 'Review']

    # Basic instance methods
    def emptyline(self):
        """Handling the  emptyline + ENTER from the interpreter"""
        pass

    # Instance do_*() methods
    def do_quit(self, line):
        """
        `quit` | `EOF`: The command exits the program.
        """
        return True

    def do_EOF(self, line):
        """
        `EOF` | `quit`: The command exits the program.
        """
        return True

    def do_create(self, line):
        """
        create <class>: To creates a new instance of <class>, and saves the
        new <class> instance into a JSON file, then prints/return the
        instace id of new <class> instance.

        valid <classes>: ['BaseModel', 'User', 'State', 'City',
                          'Amenity', 'Place', 'Review']
        """
        argv = line.split()
        if len(argv) == 0:
            print("** class name missing **")
        elif len(argv) >= 1 and argv[0] not in self.valid_classes:
            print("** class doesn't exist **")
        else:
            obj = eval("{}()".format(argv[0]))
            obj.save()
            print(obj.id)

    def do_show(self, line):
        """
        show <class> <instance id>: Printing the string representation
        of the instance with matching `instance id`.

        valid <classes>: ['BaseModel', 'User', 'State', 'City',
                          'Amenity', 'Place', 'Review']
        """
        argv = line.split()
        if len(argv) == 0:
            print("** class name missing **")
        elif len(argv) >= 1 and argv[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        else:
            # Print the string representation of the object
            storage.reload()
            objs = storage.all()
            key = "{}.{}".format(argv[0], argv[1])
            try:
                obj = objs[key]
                print(obj)
            except KeyError:
                print("** no instance found **")

    def do_destroy(self, line):
        """
        destroy <class> <instance id>: To destroy the object instance
        of with the matching `instance id`.

        valid <classes>: ['BaseModel', 'User', 'State', 'City',
                          'Amenity', 'Place', 'Review']
        """
        argv = line.split()
        if len(argv) == 0:
            print("** class name missing **")
        elif len(argv) >= 1 and argv[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        else:
            #
            # Destroy macthing instance following these stages:
            #
            objs = storage.all()
            key = "{}.{}".format(argv[0], argv[1])
            try:
                del objs[key]
                storage.save()
            except KeyError:
                print("** no instance found **")

    def do_all(self, line):
        """
        all [class]: Printing the list containing string representation
        of all instances in the storage path, optional `[class]` name
        can be passed to print only a list of  matching object with
        the class.

        valid <classes>: ['BaseModel', 'User', 'State', 'City',
                          'Amenity', 'Place', 'Review']
        """
        argv = line.split()
        if len(argv) >= 1 and argv[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(argv) >= 1 and argv[0] in self.valid_classes:
            # Print a list containing only specified class objects
            return_list = []
            storage.reload()
            objs = storage.all()
            for key, obj in objs.items():
                if key == ("" + argv[0] + "." + obj.__dict__["id"]):
                    return_list.append(obj.__str__())
            print(return_list)
        else:
            # Print a list containing all class objects in storage
            return_list = []
            storage.reload()
            objs = storage.all()
            for key, obj in objs.items():
                return_list.append(obj.__str__())
            print(return_list)

    def do_update(self, line):
        """
        update <class> <instance id> <attribute name> <attribute value>:
        Updates matching instance with a new or existing attribute.

        valid <classes>: ['BaseModel', 'User', 'State', 'City',
                          'Amenity', 'Place', 'Review']
        """
        argv = line.split()
        if len(argv) == 0:
            print("** class name missing **")
        elif len(argv) >= 1 and argv[0] not in self.valid_classes:
            print("** class doesn't exist **")
        elif len(argv) == 1:
            print("** instance id missing **")
        elif len(argv) == 2:
            print("** attribute name missing **")
        elif len(argv) == 3:
            print("** value missing **")
        else:
            # Update macthing instance while assuming:
            # + arguments are always in the right order
            # + Each arguments are separated by a space
            # + String argument with a space must be between quotes
            #
            try:
                storage.reload()
                objs = storage.all()
                key = "{}.{}".format(argv[0], argv[1])
                obj = objs[key]
                try:
                    Type = type(obj.__dict__[argv[2]])
                    obj.__dict__[argv[2]] = Type(argv[3].strip("\""))
                except KeyError:
                    obj.__dict__[argv[2]] = argv[3].strip("\"")
                obj.save()
            except KeyError:
                print("** no instance found **")

    def parseline(self, line):
        """
        To Parse every line before returning it back to the console.
        Looking out for match such as the following for extra
        processing:
        + <class name>.all()
        + <class name>.count()
        + <class name>.show(<id>)
        + <class name>.destroy(<id>)
        + <class name>.update(<id>, <attribute name>, <attribute value>)
        + <class name>.update(<id>, <dictionary representation>)
        """
        lone_commands = ['all', 'quit', 'EOF', 'help']
        argv = line.split()
        matched = re.search(r"\w+\.\w+\(", line)

        if len(argv) == 0:  # Handles empty line
            return line, line, line

        if (len(argv) != 1 or argv[0] in lone_commands) and not matched:
            # Do for commands that required arguements or
            # commands that works alone.
            return argv[0], " ".join(argv[1:]), line

        # Additional parsing for aliases listed in string doc.
        # example: class.command(args)
        if matched:
            _class, argv = line.split(".", 1)  # ['class', 'command(args)']
            cmd, argv = argv.split("(", 1)  # ['command', 'args)']
            argv = argv.replace(")", '')  # 'args)' -> 'args'

            matched = re.search(r"{.+}", argv)  # checking for dict definition
            if matched:  # if dictionary exists in arguements
                objs = storage.all()
                import json
                obj_id, argv_dict = argv.split(", ", 1)  # ['<id>', '<dict>']
                argv_dict = argv_dict.replace("'", "\"")
                obj_id = obj_id.replace("\"", "")
                argv_dict = json.loads(argv_dict)
                key = "{}.{}".format(_class, obj_id)
                try:
                    obj = objs[key]
                    obj.__dict__.update(argv_dict)
                    obj.save()
                except KeyError:
                    print("** no instance found **")

                line = ""
                return line, line, line

            if cmd == "count":  # handles <class>.count()
                objs = storage.all()
                count = 0
                for key, obj in objs.items():
                    if obj.__class__.__name__ == _class:
                        count = count + 1
                print(count)
                line = ''
                return line, line, line
            return cmd, _class + " " + " ".join(argv.split(", ")), line

        return argv[0], " ".join(argv[1:]), line


if __name__ == '__main__':
    HBNBCommand().cmdloop()
