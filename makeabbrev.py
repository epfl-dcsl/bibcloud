#!/usr/bin/python3

#####
##### generates the dblp-abbrev file
##### 
##### 
import sys

global F


#last year should normally be current year + 1
#use it as the end of range only for conferences that are assumed to happen annually going forward

MAXYEAR  = 2023

OCCURENCE_TABLE = [
    "th","st","nd","rd","th","th","th","th","th","th","th"
]

ROMAN_TABLE = [
    "TOO_STUPID_TO_INVENT_ZERO",
    "I","II","III","IV","V","VI","VII","VIII","IX","X",
    "XI","XII","XIII","XIV","XV","XVI","XVII","XVIII","XIX","XX",
    "XXI","XXII","XXIII","XXIV","XXV","XXVI","XXVII","XXVIII","XXIX","XXX"
]

# Note: the first item indicates whether the long name is a YEAR or an OCCURENCE (e.g. 1st, 2nd, ...74th...)
# 'r' is for roman, 'y' for year, 'o' for occurrence
CONF = {
    'sigcomm'   : ['y', "Proceedings of the ACM SIGCOMM YEAR Conference"],
    'sigmetrics': ['y', "Proceedings of the YEAR ACM SIGMETRICS International Conference on Measurement and Modeling of Computer Systems"],
    'sosp'      : ['o', "Proceedings of the OCCURENCE ACM Symposium on Operating Systems Principles (SOSP)"],
    'osdi'      : ['o', "Proceedings of the OCCURENCE Symposium on Operating System Design and Implementation (OSDI)"],
    'isca'      : ['o', "Proceedings of the OCCURENCE International Symposium on Computer Architecture (ISCA)"],
    'nsdi'      : ['o', "Proceedings of the OCCURENCE Symposium on Networked Systems Design and Implementation (NSDI)"],
    'asplos'    : ['r', "Proceedings of the OCCURENCE International Conference on Architectural Support for Programming Languages and Operating Systems (ASPLOS-ROMAN)"],
    'hotos'     : ['r', "Proceedings of The OCCURENCE Workshop on Hot Topics in Operating Systems (HotOS-ROMAN)"],
    'hotnets'   : ['r', "Proceedings of The OCCURENCE ACM Workshop on Hot Topics in Networks (HotNets-ROMAN)"],
    'sc'        : ['y', "Proceedings of the YEAR ACM/IEEE Conference on Supercomputing (SC)"],
    'conext'    : ['y', "Proceedings of the YEAR ACM Conference on Emerging Networking Experiments and Technology (CoNEXT)"],
    'imc'       : ['o', "Proceedings of the OCCURENCE ACM SIGCOMM Workshop on Internet Measurement (IMC)"],
    'socc'      : ['y', "Proceedings of the YEAR ACM Symposium on Cloud Computing (SOCC)"],
    'icpp'      : ['y', "Proceedings of the YEAR International Conference on Parallel Processing (ICPP)"],
    'usenix'    : ['y', "Proceedings of the YEAR USENIX Annual Technical Conference (ATC)"],
    'pldi'      : ['y', "Proceedings of the ACM SIGPLAN YEAR Conference on Programming Language Design and Implementation (PLDI)"],
    'eurosys'   : ['y', "Proceedings of the YEAR EuroSys Conference"],
    'islped'    : ['y', "Proceedings of the YEAR International Symposium on Low Power Electronics and Design"],
    'hpca'      : ['o', "Proceedings of the OCCURENCE IEEE Symposium on High-Performance Computer Architecture (HPCA)"],
    'micro'     : ['o', "Proceedings of the OCCURENCE Annual IEEE/ACM International Symposium on Microarchitecture (MICRO)"],
    'apsys'     : ['y', "Proceedings of the YEAR Asia-Pacific Workshop on Systems (APSys)"],
    'ppopp'     : ['o', "Proceedings of the OCCURENCE ACM SIGPLAN Symposium on Principles and Practice of Parallel Programming (PPoPP)"],
    'wsdm'      : ['o', "Proceedings of the OCCURENCE International Conference on Web Search and Web Data Mining (WSDM)"],
    'iptps'     : ['o', "Proceedings of the OCCURENCE International Conference on Peer-to-peer systems (IPTPS)"],
    'podc'      : ['o', "Proceedings of the OCCURENCE Annual ACM Symposium on Principles of Distributed Computing (PODC)"],
    'icac'      : ['o', "Proceedings of the OCCURENCE International Conference on Autonomic Computing (ICAC)"],
    'acsac'     : ['o', "Proceedings of the OCCURENCE International Conference on Autonomic Computing (ICAC)"],
    'fast'      : ['o', "Proceedings of the OCCURENCE USENIX Conference on File and Storage Technologie (FAST)"],
    'pdp'       : ['o', "Proceedings of the OCCURENCE Euromicro International Conference on Parallel, Distributed, and Network-Based Processing (PDP)"],
    'acsac'     : ['o', "Proceedings of the OCCURENCE Annual Computer Security Applications Conference (ACSAC)"],
    'hotsdn'    : ['o', "Proceedings of the OCCURENCE  workshop on Hot topics in software defined networking (HotSDN)"],
    'infocom'   : ['y', "Proceedings of the YEAR IEEE Conference on Computer Communications (INFOCOM)"],
    'ipdps'     : ['o', "Proceedings of the OCCURENCE IEEE International Symposium on Parallel and Distributed Processing (IPDPS)"],
    'icde'      : ['o', "Proceedings of the OCCURENCE IEEE International Conference on Data Engineering (ICDE)"],
    'hotdep'    : ['o', "Proceedings of the OCCURENCE Workshop on Hot Topics in System Dependability (HotDep)"],
    'dsn'       : ['o', "Proceedings of the OCCURENCE Annual IEEE/IFIP International Conference on Dependable Systems and Networks (DSN)"],
    'vee'       : ['o', "Proceedings of the OCCURENCE International Conference on Virtual Execution Environments (VEE)"],
    'wmcsa'     : ['o', "Proceedings of the OCCURENCE IEEE Workshop on Mobile Computing Systems and Applications"],
    'iccd'      : ['o', "Proceedings of the OCCURENCE International IEEE Conference on Computer Design (ICCD)"],
    'hpcc'      : ['y', "Proceedings of the YEAR IEEE International Conference on High Performance Computing and Communications (HPCC)"],
    'ishpc'     : ['o', "Proceedings of the OCCURENCE International Symposium on High-Performance Computing (ISHPC)"],
    'sensys'    : ['o', "Proceedings of the OCCURENCE International Conference on Embedded Networked Sensor Systems (Sensys)"],
    'lisa'      : ['o', "Proceedings of the OCCURENCE Large Installation System Administration Conference (LISA)"],
    'pact'      : ['o', "Proceedings of the OCCURENCE International Conference on Parallel Architecture and Compilation Techniques (PACT)"],
    'sigcse'    : ['o', "Proceedings of the OCCURENCE SIGCSE Technical Symposium on Computer Science Education (SIGCSE)"],
    'ispass'    : ['y', "Proceedings of the YEAR IEEE International Symposium on Performance Analysis of Systems and Software (ISPASS)"],
    'fpl'       : ['o', "Proceedings of the OCCURENCE International Conference on Field Programmable Logic and Applications (FPL)"],
    "threepgcic" : ['o', "Proceedings of the OCCURENCE International Conference on P2P, Parallel, Grid, Cloud and Internet Computing (3PGCIC)"],
    "mobicom"   : ['o', "Proceedings of the OCCURENCE Annual International Conference on Mobile Computing and Networking (MobiCom)"],
    "bigdata" : ['y', "Proceedings of the YEAR IEEE Conference on Big Data"],
    "inflow"  : ['o', "Proceedings of the OCCURENCE Workshop on Interactions of NVM/FLASH with Operating Systems and Workload (INFLOW)"] ,
    "ndss"    : ['y', "Proceedings of the YEAR Annual Network and Distributed System Security Symposium (NDSS)"],
    "popl"    : ['o', "Proceedings of the OCCURENCE ACM SIGPLAN Symposium on Principles of Programming Languages (POPL)"],
    "uss"     : ['o', "Proceedings of the OCCURENCE USENIX Security Symposium"],
    "stoc"    : ['o', "Proceedings of the OCCURENCE ACM Symposium on the Theory of Computing (STOC)"],
    "www"     : ['o', "Proceedings of the OCCURENCE International Conference on World Wide Web (WWW)"],
    "icdcs"   : ['o', "Proceedings of the OCCURENCE IEEE International Conference on Distributed Computing Systems (ICDCS)"],
    "iiswc"   : ['y', "Proceedings of the YEAR IEEE International Symposium on Workload Characterization (IISWC)"],
    "spaa"    : ['o', "Proceedings of the OCCURENCE ACM Symposium on Parallelism in Algorithms and Architectures (SPAA)"],
    "vldb"     : ['o', "Proceedings of the OCCURENCE International Conference on Very Large DataBases (VLDB)"],
    "sigcse"  : ['o', "Proceedings of the OCCURENCE ACM Technical Symposium on Computer Science Education (SIGCSE)"],
    "hoti"    : ['y', "Proceedings of the YEAR Annual Symposium on High-Performance Interconnects"],
    "rtas"    : ['y', "Proceedings of the YEAR Real-Time and Embedded Technology and Applications Symposium"],
    'hotcloud'    : ['o', "Proceedings of the OCCURENCE  workshop on Hot topics in Cloud Computing (HotCloud)"],
    "cloud" : ['o', "Proceedings of the OCCURENCE IEEE International Conference on Cloud Computing (CLOUD)"],
    "woot" : ['o', "Proceedings of the OCCURENCE {USENIX} Workshop on Offensive Technologies (WOOT)"],
    "iwmm"  : ['y',"Proceedings of the YEAR International Workshop on Memory Management (IWMM)"],
    "ismm"  : ['o',"Proceedings of the OCCURENCE International Symposium on Memory Management (ISMM)"],
    "cidr"  : ['o',"Proceedings of the OCCURENCE Biennial Conference on Innovative Data Systems Research (CIDR)"],
    "sosr"  : ['y',"Proceedings of the Symposium on SDN Research (SOSR)"],
    "lcn"   : ['o',"Proceedings of the OCCURENCE IEEE Conference on Local Computer Networks (LCN)"],
    "wren"  : ['o',"Proceedings of the OCCURENCE ACM SIGCOMM 2009 Workshop on Research on Enterprise Networking (WREN)"],
    "simpar" : ['y', "Proceedings of the YEAR IEEE International Conference on Simulation, Modeling, and Programming for Autonomous Robots (SIMPAR)"],
    "nips"   : ['y', "Proceedings of the YEAR Annual Conference on Neural Information Processing Systems (NIPS)"],
    "kbnets@sigcomm" : ['y',"Proceedings of the YEAR Workshop on Kernel-Bypass Networks (KBNETS@SIGCOMM)"],
    "sigir" : ['o', "Proceedings of the OCCURENCE International ACM SIGIR conference on Research and Development in Information Retrieval (SIGIR)"],
    "ccgrid" : ['o', "Proceedings of the OCCURENCE IEEE/ACM International Symposium on Cluster, Cloud and Grid Computing (CCGRID)"],
    "networking" : ['y', "Proceedings of the YEAR IFIP Networking Conference"],
    "apnet"  : ['o', "Proceedings of the OCCURENCE Asia-Pacific Workshop on Networking (APNet)"],
    "focs" : ['o', "Proceedings of the OCCURENCE IEEE Annual Symposium on Foundations of Computer Science (FOCS)"],
    "mapl@pldi": ['o', "Proceedings of the OCCURENCE ACM SIGPLAN International Workshop on Machine Learning and Programming Languages (MAPL@PLDI)"],
    "bcb": ['o', "Proceedings of the OCCURENCE ACM International Conference on Bioinformatics, Computational Biology,and Health Informatics"],
    "hilt": ['y', "Proceedings of the YEAR ACM SIGAda annual conference on High integrity language technology"],
    "minenet": ['o', "Proceedings of the OCCURENCE Annual ACM Workshop on Mining Network Data (MineNet)"],
    "memsys" : ['y', "Proceedings of the YEAR International Symposium on Memory Systems (MEMSYS)"],
    "oopsla" : ['o', "Proceedings of the OCCURENCE Annual ACM SIGPLAN Conference on Object-Oriented Programming, Systems, Languages, and Applications (OOPSLA)"],
    "srds"   : ['o', "Proceedings of the OCCURENCE IEEE Symposium on Reliable Distributed Systems (SRDS)"],
    "icnp"   : ['o', "Proceedings of the OCCURENCE IEEE International Conference on Network Protocols (ICNP)"],
    "icdcs"  : ['o', "Proceedings of the OCCURENCE IEEE International Conference on Distributed Computing Systems (ICDCS)"],
    "hpdc"   : ['o', "Proceedings of the OCCURENCE International Symposium on High-Performance Parallel and Distributed Computing (HPDC)"],
    "hpts"   : ['y', "Proceedings of the YEAR International Workshop on High-Performance Transaction Systems (HTPS)"],
    "middleware" : ['y',"Proceedings of the YEAR International Middleware Conference"],
    "adms@vldb" : ['y', "Proceedings of the International Workshop on Accelerating Analytics and Data Management Systems Using Modern Processor and Storage Architectures (ADMS@VLDB)"],
    "globecom" : ['y', "Proceedings of the YEAR IEEE Global Communications Conference (GLOBECOM)"],
    "pam" : ['o', "Proceedings of the OCCURENCE International Conference on Passive and Active Measurement (PAM)"],
    "icc" : ['y', "Proceedings of the YEAR IEEE International Conference on Communications (ICC)"],
    "hotmiddlebox@sigcomm" : ['y',"Proceedings of the YEAR ACM SIGCOMM Workshop on Hot topics in Middleboxes and Network Function Virtualization (HotMiddlebox@SIGCOMM)"],
    "ndm@sc" : ['o',"Proceedings of the OCCURENCE International Workshop on Network-Aware Data Management (NDM@SC)"],
    "raid" : ['o',"Proceedings of the OCCURENCE International Symposium on Research in Attacks, Intrusions, and Defenses(RAID)"],
    "bs" : ['y',"Proceedings of the YEAR Workshop on Buffer Sizing"],
    "ancs" : ['y',"Proceedings of the YEAR ACM/IEEE Symposium on Architectures for Networking and Communications Systems (ANCS)"],
    "uai" :['o',"Proceedings of the OCCURENCE Conference on Uncertainty in Artificial Intelligence (UAI)"],
    "usits" : ['o',"Proceedings of the OCCURENCE USENIX Symposium on Internet Technologies and Systems (USITS)"],
    "ccs" : ['y',"Proceedings of the YEAR ACM SIGSAC Conference on Computer and Communications Security (CCS)"],
    "eurosec" : ['o',"Proceedings of the OCCURENCE European Workshop on Systems Security (EUROSEC)"],
    "opodis" : ['o',"Proceedings of the OCCURENCE International Conference on Principles of Distributed Systems (OPODIS)"]
}

SHORTCONF = {
    'usenix' : 'USENIX ATC'
}


def make_sigcomm(conf,year):
    global CONF, outtype,SHORTCONF

    c = CONF[conf]
    if c[0] != 'y':
        print("conf mismatch ",conf)
        sys.exit(1)
    s = c[1]

    yy = year % 100
    ss = s.replace("YEAR", '%02d' % year) 

    if outtype == "short":
        confstr = conf.upper()
        if conf in SHORTCONF: 
            shortconf = confstr = SHORTCONF[conf]

        return "@string{"+conf+ '%02d' % yy +" = \"" + confstr + "\"}\n"

    return "@string{"+conf+ '%02d' % yy +" = \"" +ss + "\"}\n"

def make_sosp(conf,year,occurence):
    global CONF
    c = CONF[conf]
    if c[0] != 'o':
        print("conf mismatch ",conf)
        sys.exit(1)
    s = c[1]

    yy = year % 100
    if occurence>=11 and occurence <14:
        occ = str(occurence) +"th"
    else: 
        occ = str(occurence) + OCCURENCE_TABLE[occurence%10]
    
    ss = s.replace("OCCURENCE",occ)
    if outtype == "short":
        return "@string{"+conf+ '%02d' % yy +" = \"" +conf.upper() +  "\"}\n"

    return "@string{"+conf+'%02d'%yy+" = \"" +ss + "\"}\n"
    
def make_asplos(conf,year,occurence):
    global CONF

    c = CONF[conf]
    if c[0] != 'r' :
        print("conf mismatch ",conf)
        sys.exit(1)

    s = c[1]
    yy = year % 100
    if occurence>11 and occurence <14:
        occ = str(occurence) +"th"
    else:
        occ = str(occurence) + OCCURENCE_TABLE[occurence%10]
    ss = s.replace("OCCURENCE",occ)
    ss = ss.replace("ROMAN",ROMAN_TABLE[occurence])
    if outtype == "short":
        return "@string{"+conf+ '%02d' % yy +" = \"" +conf.upper() + "-" + ROMAN_TABLE[occurence] + "\"}\n"

    return "@string{"+conf+'%02d'%yy+" = \"" +ss + "\"}\n"



#################################################
# generate ranges
#################################################

def annual_occ(k,first_occ,first_y,end_y):
    occ = first_occ
    for y in range(first_y,end_y):
        F.write(make_sosp(k,y,occ))
        occ = occ +1
    

def annual_year(k,first_y,end_y):
    for y in range(first_y,end_y):
        F.write(make_sigcomm(k,y))
    

    
###################################################
# main
###################################################

if len(sys.argv) == 1:
    outtype = "long"
elif len(sys.argv) == 2:
    outtype = sys.argv[1]
else:
    print("bad argv\n")
    sys.exit(1)

if outtype == "long":
    F = open("gen-abbrev.bib","w")    
elif outtype == "short":
    F = open("gen-abbrev-short.bib","w")    
else:
    print("output is either long or short\n")
    sys.exit(1)


F.write("%%% AUTOMATICALLY GENERATED BY make-abbrev.py\n")
F.write("%%% DO NOT EDIT\n")

for y in range(1988,MAXYEAR):
    F.write(make_sigcomm("sigcomm",y))


for y in range(1993,2017):
    F.write(make_sigcomm("sigmetrics",y))


for occ in range (1,32):
    y = 1967 + (occ-1)*2
    F.write(make_sosp("sosp",y,occ))


F.write(make_sosp("osdi",1996,2))
F.write(make_sosp("osdi",1999,3))
for occ in range (4,15):
    y = 2000 + (occ-4)*2
    F.write(make_sosp("osdi",y,occ))


annual_occ("isca",17,1990,MAXYEAR)
annual_occ("nsdi",1,2004,MAXYEAR)
annual_occ("pam",8,2007,2020)

annual_year("icc",2000,2019)

for occ in range (5,13):
    y = 1992 + (occ-5)*2
    F.write(make_asplos("asplos",y,occ))

occ = 13
for y in range(2008,2022):
    F.write(make_asplos("asplos",y,occ))
    occ = occ +1

for occ in range (6,18):
    y = 1997 + (occ-6)*2
    F.write(make_asplos("hotos",y,occ))

for occ in range (6,20):
    y = 2007 + (occ-6)
    F.write(make_asplos("hotnets",y,occ))


for y in range (1993,2018):
    F.write(make_sigcomm("sc",y))

annual_occ("ndm@sc",3,2013,2016)
annual_year("conext",2005,MAXYEAR)
annual_occ("imc",1,2001,2016)
annual_year("socc",2010,MAXYEAR)


for occ in range (1,10):
    y = 2005 + occ
    F.write(make_sigcomm("icpp",y))

for occ in range (1,30):
    y = 1994 + occ
    F.write(make_sigcomm("usenix",y))

for y in range (1990,2018): 
    F.write(make_sigcomm("pldi",y))


for y in range(2006,2022):
    F.write(make_sigcomm("eurosys",y))

for y in range (2010,2011):
    F.write(make_sigcomm("islped",y))

for y in range(2017,2020):
    F.write(make_sigcomm("kbnets@sigcomm",y))

for y in range(2016,2018):
    F.write(make_sigcomm("hotmiddlebox@sigcomm",y))


annual_occ("hpca",1,1995,2019)
annual_occ("micro",1,1968,2020)



for y in range (2010,2017):
    F.write(make_sigcomm("apsys",y))


annual_occ("ppopp",10,2005,2019)
annual_occ("wsdm",1,2008,2017)
annual_occ("iptps",1,2002,2017)
annual_occ("podc",1,1982,2017)
annual_occ("icac",1,2004,2017)
annual_occ("fast",5,2007,2020)


### careful - pdp changes from conference to workshop
occ = 14
for y in range(2006,2017):
    F.write(make_sosp("pdp",y,occ))
    occ = occ+1

CONF['pdp'] = ['o', "Proceedings of the OCCURENCE Euromicro Workshop on Parallel, Distributed and Network-Based Processing (PDP)"]
occ = 1
for y in range (1993,2006):
    F.write(make_sosp("pdp",y,occ))
    occ = occ+1

annual_occ("acsac",10,1994,2017)
annual_occ("hotsdn",1,2012,2017)
annual_occ("hotcloud",1,2009,MAXYEAR)


for y in range (1989,2017):
    F.write(make_sigcomm("infocom",y))

annual_occ("ipdps",24,2010,2021)
annual_occ("icde",31,2015,2017)
annual_occ("hotdep",2,2006,2016)
annual_occ("dsn",36,2006,MAXYEAR)
annual_occ("vee",1,2005,2016)
annual_occ("wmcsa",4,2002,2004)
annual_occ("iccd",23,2005,2015)

occ = 1
for y in range (2005,2018):
    F.write(make_sigcomm("hpcc",y))
    occ = occ+1

occ = 1
for y in range (2005,2018):
    F.write(make_sigcomm("hoti",y))
    occ = occ+1

occ = 1
for y in range (2005,2018):
    F.write(make_sigcomm("rtas",y))
    occ = occ+1

F.write(make_sosp("ishpc",2000,3))

annual_occ("sensys",1,2003,2016)
annual_occ("lisa",10,1996,2016)
annual_occ("pact",6,1997,2018)
annual_occ("sigcse",36,2005,2006)

annual_year("ispass",2000,2017)
annual_occ("fpl",11,2001,2017)    #was a workshop earlier
annual_occ("threepgcic",5,2010,2017)
annual_occ("mobicom",6,2000,2017)

annual_year("bigdata",2012,2018)
annual_occ("inflow",1,2013,2017)
annual_year("ndss",1995,MAXYEAR)
annual_occ("popl",15,1988,2018)

F.write(make_sosp("uss",1996,6))
annual_occ("uss",7,1998,2020)


annual_occ("stoc",1,1969,2018)

annual_occ("www",1,1994,2018)
annual_occ("icdcs",20,2000,2018)
annual_year("iiswc",2006,2018)
annual_occ("spaa",12,2000,2018)
annual_occ("vldb",26,2000,2020)
annual_occ("vldb",5, 1979, 1980)

annual_occ("sigcse",42,2011,2012)
annual_occ("cloud",2,2009,MAXYEAR)
annual_occ("woot",4,2010,2018)
annual_year("sosr",2015,2019)
annual_occ("lcn",38,2013,2019)
annual_occ("wren",1,2009,2010)
annual_year("simpar",2008,2018)
annual_year("nips",2010,2018)
annual_year("hilt", 2014,2015)
annual_occ("focs",41,2000,2001)
annual_year("kbnets@sigcomm",2016,2019)
annual_occ("sigir",35,2012,2019)
annual_occ("ccgrid",10,2010,2019)
annual_occ("mapl@pldi",1,2017,2018)
annual_occ("bcb",8,2017,2018)
annual_occ("minenet",1,2005,2008)
annual_year("memsys",2015,2020)
annual_occ("srds",25,2006,2020)
annual_occ("icnp",18,2010,2020)
annual_occ("icdcs",11,1991,2020)
annual_occ("hpdc",24,2015,2020)
annual_year("hpts",1985,1986)
annual_year("middleware",2000,2020)
annual_year("adms@vldb",2000,2020)
annual_year("globecom",2017,2020)
annual_occ("raid",4,2001,MAXYEAR)
annual_year("bs",2019,2020)
annual_year("ancs",2016,MAXYEAR)
annual_occ("uai",26,2010,2020)
annual_occ("apnet",1,2017,MAXYEAR)
annual_year("ccs",2005,MAXYEAR)
annual_occ("eurosec",7,2014,MAXYEAR)
annual_occ("opodis",10,2006,MAXYEAR)

#crazy ones:
annual_year("iwmm",1992,1996)
annual_occ("ismm",4,2004,2005)
annual_year("networking",2010,2019)
annual_occ("oopsla",15,2000,2019)

for occ in range (1,10):
    y = 2001 + occ*2
    F.write(make_sosp("cidr",y,occ))

for occ in range (1,5):
    y = 1995 + occ*2
    F.write(make_sosp("usits",y,occ))

F.close()
