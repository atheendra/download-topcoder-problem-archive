import urllib
import urllib2
import string
import sys
import os
from subprocess import call
from BeautifulSoup import BeautifulSoup
from optparse import OptionParser


def get_soup(link):
    response = urllib2.urlopen(link)
    html_page = response.read()
    pool = BeautifulSoup(html_page)
    return pool


def get_ids_from_website(link):
    problem_ids = []
    pool = get_soup(link)
    results = pool.findAll('a', attrs={'class' : 'statText'})

    for result in results:
        href_link = result['href']
        if problem_statement_pattern in href_link:
            problem_ids.append(
                    href_link.replace(problem_statement_pattern,""))
    return problem_ids


def get_completed_problem_ids(file):
    infile = open(file, "r")
    completed_ids = []

    for line in infile.readlines():
        if line is not "\n":
            completed_ids.append(line.rstrip())
    infile.close()
    return completed_ids


def download_single_id(id, completed_ids_file):
    exit_status = call(["gettc", id])
    if exit_status is 0:
        with open(completed_ids_file, "a") as outfile:
            outfile.writelines(id + "\n")
    else:
        print("Error in downloading ID " + id)


def download_new_ids(link, completed_ids_file):
    completed_ids = get_completed_problem_ids(completed_ids_file)
    current_ids = get_ids_from_website(link)
    download_ids = [ id for id in current_ids if id not in completed_ids ]

    os.chdir(destination_dir)
    for id in download_ids:
        download_single_id(id, completed_ids_file) 


def construct_link_from_options():
    if options.link is None:
        topcoder_options["er"] = str(options.n)
        if options.category in problem_categories:
            urlified_cat = str(options.category).replace("/", "%2F").replace(" ","+")
            topcoder_options["cat"] = urlified_cat
        else:
            print "Invalid Category specified. Valid categories are:"
            print ",".join(problem_categories)
            exit(1)
        topcoder_options["div1l"] = str(options.d1)
        topcoder_options["div2l"] = str(options.d2)


        link_options = []
        for o, v in topcoder_options.iteritems():
            link_options.append(o + "=" + v)
        link = base_link + "&" + "&".join(link_options)
    return link


user_agent = 'Mozilla/5 (Solaris 10) Gecko'
headers = { 'User-Agent' : user_agent }

#Global variables
base_link = "http://community.topcoder.com/tc?module=ProblemArchive"
problem_statement_pattern = "/stat?c=problem_statement&pm="
destination_dir = ""
completed_ids_file = "~/problem_ids.txt"
topcoder_options = {"sr":"", "er":"", "sc":"", "sd":"", "class":"",
                    "cat":"", "div1l":"", "div2l":"", "mind1s":"",
                    "mind2s":"", "maxd1s":"", "maxd2s":"", "wr":""}
problem_categories = ["", "Advanced Math", "Brute Force", 
                      "Dynamic Programming", "Encryption/Compression",
                      "Geometry", "Graph Theory", "Greedy", "Math", 
                      "Recursion", "Search", "Simple Math", "Simple Search",
                      "Iteration", "Simulation", "Sorting", 
                      "String Manipulation", "String Parsing"]

parser = OptionParser()
parser.add_option("-l", "--link", dest="link",
                  help="Link of the Topcoder archive website to download."
                       + "If specified, all other link-options like -n, -t "
                       + "are ignored",
                  default=None)
parser.add_option("-d", "--destination", dest="destination_dir",
                  help="Destination to download problems",
                  default="~/Topcoder")
parser.add_option("-c", "--completed_list", dest="completed_ids",
                  help="File containing list of problem IDs that should not "
                       + "be downloaded",
                  default=None)
parser.add_option("-n", "--number_of_problems", dest="n",
                  help="Number of problems to download (Used only when link"
                       +" is not specified)", default=1000)
parser.add_option("--d1", dest="d1",
                  help="Division I Level (Used only when link is "
                       + "not specified)", default="")
parser.add_option("--d2", dest="d2",
                  help="Division II Level (Used only when link is "
                       + "not specified)", default="")
parser.add_option("-t", "--category", dest="category",
                  help="Category (Used only when link is "
                       + "not specified)", default="")

(options, args) = parser.parse_args()
link = construct_link_from_options()
destination_dir = options.destination_dir
completed_ids = options.completed_ids

download_new_ids(link, completed_ids_file)
