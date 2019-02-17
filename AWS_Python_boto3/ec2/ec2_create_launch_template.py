def launch_instance():
    input = ""

    while True:
        input = raw_input("\nLaunch Instance Menu\n\nEnter the OS would you like to start an instance with\n\n 1. Windows\n 2. Linux\n 0. Back\n\n> ").lower()

        if input in ("windows", "w", "win", "1"):
            image = "ami-d4228ea3"
            launch("Windows", image)

        elif input in ("linux", "l", "lin", "2"):
            image = ""
            launch("Linux", image)

        elif input in ("exit", "e", "b", "back", "0")
            return

        else:
            print "\n\nInvalid option!\n\n"

def launch(type, image):
    input = raw_input("\nCreate " + type + " instance with image: " + image + "? (Y/N) ").lower()
    if input in ("y", "yes"):
        instance = conn.run_instances(image, key_name="Abhinav2018", instance_type="t2.micro")
        print "\nStarting new EC2 instance id: %s \n" % instance.id
    else:
        return