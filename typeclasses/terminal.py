from typeclasses.objects import Object
from evennia import default_cmds
from evennia.utils.evmenu import EvMenu

# Time based payment

class Terminal(Object):
    """
    All terminals should be based on this object.
    """
    def at_object_creation(self):
        self.db.desc = "This is a terminal."
        self.db.screen_buffer = []
        self.db.affiliation = "The Limbo"
        self.db.employees = []
        self.db.jobs = [
            {
                "family":"owner",
                "ranks": 1,
                "rank_titles":["Owner"],
                "pay": [0],
                "available": 1,
                "privledge": 3
            },
            {
                "family":"manager",
                "ranks": 1,
                "rank_titles":["Manager"],
                "pay": [3000],
                "available": 1,
                "privledge": 2
            },
            {
                "family": "bartender",
                "ranks": 3,
                "rank_titles": ["Junior Bartender", "Bartender", "Senior Bartender"],
                "pay": [1000, 1750, 2000],
                "available": 2,
                "privledge": 1
            },
            {
                "family": "dancer",
                "ranks": 3,
                "rank_titles": ["Junior Dancer", "Dancer", "Pro Dancer"],
                "pay": [1000, 1750, 2000],
                "available": 3,
                "privledge": 0
            }
        ]

    def on_use(self, caller):
        if caller.db.employment and caller.db.employment["employer"] == self.db.affiliation or "admin" in str(caller.permissions):
            caller.ndb.terminal = self
            EvMenu(caller, "typeclasses.terminal", startnode="menu_start", cmd_on_exit="")
        else:
            caller.msg(f"The {self} buzzes angrily as you run out of login attempts.")
            caller.location.msg_contents(f"The {self} buzzes angrily as {caller} runs out of login attempts.", exclude=caller)

def menu_start(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    caller.msg(f"You log into the {terminal}", exclude=caller)
    caller.location.msg_contents(f"{caller} logs into the {terminal}.", exclude=caller)
    text = \
    f"""
    {terminal}: Main Menu
    """
    options = (
        {"desc": "My Record","goto": "menu_record"},
        {"desc": "Collect Pay","goto": "menu_collect_pay"},
        {"desc": "Manager Menu","goto": "menu_employees"},
        {"desc": "Logout","goto":"quit_terminal"}
    )
    return text, options
def menu_record(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    job = find_job(caller.db.employment["job_family"], caller)
    text = "Your employment record:"
    text += "\n\tJob family: "+job["family"].title()
    text += "\n\t Job title: "+job["rank_titles"][caller.db.employment["rank"]]
    text += "\n\t    Salary: "+str(job["pay"][caller.db.employment["rank"]])
    text += "\n\t Hire date: "+str(caller.db.employment["hired"])
    options = (
        {"desc": "Back to main menu","goto": "menu_start"},
        {"desc": "Logout","goto": "quit_terminal"},
    )
    return text, options
def menu_employees(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    access = get_access(caller)
    if access < 2:
        caller.location.msg_contents("The terminal lets out a soft beep.")
        text = "You do not have access to this menu."
        options = (
            {"desc": "Back to main menu","goto": "menu_start"},
            {"desc": "Logout","goto": "quit_terminal"},
        )
    else:
        text = "Employee Management Menu"
        options = (
            {"desc": "Available Jobs","goto": "menu_list_jobs"},
            {"desc": "Manage Employees","goto": "menu_manage_employees"},
            {"desc": "Return to Main Menu","goto": "menu_start"},
            {"desc": "Logout","goto": "quit_terminal"},
        )
    return text, options
def menu_collect_pay(caller, raw_string, **kwargs):
    import time
    import math
    period = 604800
    terminal = caller.ndb.terminal
    job = find_job(caller.db.employment["job_family"], caller)
    last_paid = caller.db.employment["last_paid"]
    cur_time = int(time.time())
    salary = job["pay"][caller.db.employment["rank"]]
    diff = last_paid - cur_time
    periods = math.floor(diff/period)

    if periods >= 1: 
        caller.db.currency += salary*periods
        caller.location.msg_contents(f"The {terminal} spits some cash out into {caller}'s hand.", exclude=caller)
        caller.msg(f"The {terminal} spits some cash out into your hand.")
        caller.db.employment["last_paid"] += period*periods
        text = f"Payment rendered: {str(salary*periods)}\nNext payment: "+str(caller.employment["last_paid"]+period)
    else:
        import datetime
        text = f"Payment not yet due.\nNext issue date: "+str(datetime.datetime.fromtimestamp(caller.db.employment["last_paid"]+period-((8*60*60)+1)).strftime('%A, %b %d at %I:%M %p'))

    return text, {"desc": "Logout","goto": "quit_terminal"},
def menu_list_jobs(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    text = ""
    for job in terminal.db.jobs:
        if job["privledge"] <= get_access(caller):
            text += job["family"].title()+" (Available: "+str(job["available"])+")\n"
            i = 0
            for title in job["rank_titles"]:
                text += f"\tTitle: {title}\tSalary: "+str(job["pay"][i])+"\n"
                i = i+1
    options = (
        {"desc": "Available Jobs","goto": "menu_list_jobs"},
        {"desc": "Add Employee","goto": "menu_add_employee"},
        {"desc": "Manage Employees","goto": "menu_manage_employees"},
        {"desc": "Return to Main Menu","goto": "menu_start"},
        {"desc": "Logout","goto": "quit_terminal"},
    )
    return text, options
def menu_manage_employees(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    text = "Current Employees:\n"
    options = [
        {"desc": "Available Jobs","goto": "menu_list_jobs"},
        {"desc": "Add Employee","goto": "menu_add_employee"}
    ]
    if len(terminal.db.employees) > 0:
        for employee in terminal.db.employees:
            text += f"\t{employee}"+" - "+employee.db.employment["job_title"][employee.db.employment["rank"]]+"\n"
        options.append({"desc": "Fire Employee","goto": "menu_fire_employee"})
    else:
        text = "\tYou don't have any employees." 
    options.append({"desc": "Return to Main Menu","goto": "menu_start"})
    options.append({"desc": "Logout","goto": "quit_terminal"})
    return text, options    
def menu_add_employee(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    text = "What job would you like to hire for?"
    options = []
    for job in terminal.db.jobs:
        if job["available"] > 0 and job["privledge"] < get_access(caller):
            options.append({"desc":job["family"].title(), "goto": ("menu_add_employee2", {"job":job["family"]})})
    
    options.append({"desc": "Return to management menu","goto": "menu_employees"})
    options.append({"desc": "Logout","goto": "quit_terminal"})
    return text, options   
def menu_add_employee2(caller, raw_string, **kwargs):
    job_family = kwargs["job"]
    text = f"Please enter the name of who you would like to hire as a {job_family} or press enter to abort."
    options = []
    options.append({
        "key":"_default",
        "goto": ("menu_add_employee3",{"job":job_family})
    })
    return text, options   
def menu_add_employee3(caller, raw_string, **kwargs):
    from evennia.utils.search import search_object
    import time
    terminal = caller.ndb.terminal
    job_family = kwargs["job"]
    target = raw_string.strip()
    char = search_object(target, typeclass="typeclasses.characters.Character")[0]
    options = []

    #Check error conditions
    if not target:
        text = "Hiring process aborted"
    elif not char:
        text = "Could not find a valid employee with that name."
    elif not char.db.employment is None:
        text = "Labor database reports that invidiual is already employed."
    else:
        #Find target job
        target_job = find_job(job_family, caller)

        #Set job details on character
        cur_time = int(time.time())
        char.db.employment = {
            "employer": terminal.db.affiliation,
            "job_family": target_job["family"],
            "job_title": target_job["rank_titles"],
            "rank": 0,
            "hired": cur_time,
            "last_paid": cur_time
        }
        char.db.affiliations.append(terminal.db.affiliation)

        #Update terminal roster
        target_job["available"] -= 1
        terminal.db.employees.append(char)

        #Done
        text = f"You have hired {char} as a {job_family}."

    options.append({"desc": "Return to management menu","goto": "menu_employees"})
    options.append({"desc": "Return to main menu","goto": "menu_start"})
    options.append({"desc": "Logout","goto": "quit_terminal"})
    return text, options   
def menu_fire_employee(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    text = "Select the employee you would like to fire."
    options = []
    for employee in terminal.db.employees:
        if not employee is caller: 
            options.append(
                {
                    "desc":employee,
                    "goto": (
                        "menu_fire_employee2", 
                        {"employee":employee}
                    )
                }
            )
    options.append({"desc": "Cancel","goto": "menu_manage_employees"},)
    return text, options
def menu_fire_employee2(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    employee = kwargs["employee"]
    text = f"Are you sure you want to fire {employee}?"
    options = [
        {
            "desc":"Confirm",
            "goto": (
                "menu_fire_employee3", 
                {"employee":employee}
            )
        },
        {"desc":"Cancel","goto":"menu_manage_employees"}
    ]
    return text, options
def menu_fire_employee3(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    employee = kwargs["employee"]
    text = f"{employee} has been fired."
    options = [{"desc":"OK","goto":"menu_manage_employees"}]

    #Get the terminal's job object for this employyee
    target_job = find_job(employee.db.employment["job_family"],caller)

    #Clear employee's job
    employee.db.employment = None
    employee.remove_affiliation(terminal.db.affiliation)

    #Update terminal roster
    target_job["available"] += 1
    terminal.db.employees.remove(employee)

    return text, options
def quit_terminal(caller, raw_string, **kwargs):
    terminal = caller.ndb.terminal
    caller.msg(f"You log out of the {terminal}", exclude=caller)
    caller.location.msg_contents(f"{caller} logs out of the {terminal}.", exclude=caller)
    caller.ndb.terminal = None
    return "", None
def find_job(target, caller):
    terminal = caller.ndb.terminal
    for job in terminal.db.jobs:
        if job["family"] == target:
            return job
    return None
def get_access(caller):
    if "admin" in str(caller.permissions): 
        return 99
    else:
        return find_job(caller.db.employment["job_family"], caller)["privledge"]