# -*- coding: utf-8 -*-
"""
Created on Sun Feb 7 23:46:27 2016

@author: vsannibale
"""

from vprint import VerbosePrint
from ContainerExtra import Container
import numpy as np
import os

class LTSpice(Container):

    RAW_Extension    = "raw"
    ASC_Extension    = "asc"
    NET_Extension    = "net"
    PLT_Extension    = "txt"
    DefaultSimulator = "ltspice"
    TimeUnits        = "s"
    TimeName         = "Time"
    UnitPrefixes     = [ "f", "p","n","u","m", "", "k","meg","g", "t"]

    def __init__(self, PathName="", *v, **kv):

        self.Path, self.FileName = os.path.split(PathName)
        self.BaseName = os.path.splitext(self.FileName)[0]
        self.BasePath = os.path.join(self.Path, self.FileName)
        self.Verbose  = 0

        Container.__init__(self,*v,**kv)



    def run(self, Extension="asc"):

        bp  = "%s.%s" %  ( self.BasePath, Extension)

        if  os.path.isfile(bp):
            s = "cd %s; wine /apps/ltspice/scad3.exe -b -ascii -Run %s.%s\n" % ( self.Path, self.FileName, Extension)
            VerbosePrint(self.Verbose,1,s)
            os.system(s)
            self.read()

        else:
            raise IOError("cannot find file \"%s\" to run the ltspice simulation" % bp )



    def units_convert(self,s):

        s = s.lower()

        if   s == "voltage"       :  return "V"
        elif s == "device_current":  return "A"
        else:                        return s


    def prefix_convert(self,s):

        s = s.lower()

        if s.find("meg") >0 :
            n = self.UnitPrefixes.index(s[-3:])
            v = float(s[:-3])
        else:
            try:
                n = self.UnitPrefixes.index(s[-1])
                v = float(s[:-1])
            except:
                n = self.UnitPrefixes.index("")
                v = float(s)

        print(10.0**(-15+3*n))

        return v*10**(-15+3*n), 10.0**(-15+3*n)


    def read_header(self):
        def lineread(f):
            return f.readline()[:-1].split(":")[-1].strip()

        with open("%s.%s" % (self.BasePath, self.RAW_Extension), "rb") as f:
            self.Title     = lineread(f)
            self.Date      = lineread(f)
            self.Analysis  = lineread(f)
            self.Flags     = lineread(f)
            self.Variables = int(lineread(f))
            self.Points    = int(lineread(f))
            self.Offset    = float(lineread(f))
            self.Command   = lineread(f)
            self.Channels  = self.Variables-1

            f.readline()

            self.Name  = []
            self.Units = []
            _, Name, Units = f.readline()[:-1].strip().split("\t")
            for n in range(self.Channels):
                _, Name, Units = f.readline()[:-1].strip().split("\t")
                self.Name.append(Name)
                self.Units.append(self.units_convert(Units))



    def read(self):

        def lineread(f):
            return f.readline()[:-1].split(":")[-1].strip()

        with open("%s.%s" % (self.BasePath, self.RAW_Extension), "rb") as f:
            self.Title     = lineread(f)
            self.Date      = lineread(f)
            self.Analysis  = lineread(f)
            self.Flags     = lineread(f)
            self.Variables = int(lineread(f))
            self.Points    = int(lineread(f))
            self.Offset    = float(lineread(f))
            self.Command   = lineread(f)
            self.Channels  = self.Variables-1

            f.readline()

            self.Name  = []
            self.Units = []
            _, Name, Units = f.readline()[:-1].strip().split("\t")
            for n in range(self.Channels):
                _, Name, Units = f.readline()[:-1].strip().split("\t")
                self.Name.append(Name)
                self.Units.append(self.units_convert(Units))

            f.readline()

            t =[];
            X =[];
            for n in range(self.Points):
                s = f.readline().strip().split("\t")
                t.append(float(s[0]))
                x = [ float(s[-1])]
                for i in range(self.Channels):
                    x.append(float(f.readline()))

                X.append(x)

        self.ltspice_tran_parameters()
        self.t = np.asarray(t,dtype=np.float64)*self.PrefixFactor
        self.x = np.asarray(X,dtype=np.float64)


    def read_multiple(self,N):

        with open("%s.%s" % (self.BasePath, self.PLT_Extension), "rb") as f:

            f.readline()
            f.readline()
            T = []
            X = []
            x = []
            t = []
            for s in f:
                if s[0] == "S":
                    T.append(t)
                    X.append(x)
                    t =[];
                    x =[];
                else:
                    s1 = s.strip().split("\t")
                    t.append(float(s1[0]))
                    x.append(float(s1[-1]))


        self.t = np.asarray(T,dtype=np.float64)
        self.x = np.asarray(X,dtype=np.float64)



    def signal_index(self,s):
        try:
           return self.Name.index(s)
        except:
           return None


    def get_channel(self, n, r=None):

         n =  self.signal_index(n) if isinstance(n, str) else n

         if r is None:
             return self.x[:, n]
         else:
             return self.x[r, n]



    def plot_channel(self, n, r=None, **kv):

        n = self.signal_index(n)

        pl.plot(self.t,self.get_channel(n,r))
        pl.xlabel( "time [%s]" % (self.TimeUnits))
        pl.ylabel("%s [%s]" % (self.Name[n],self.Units[n] ))
        pl.grid("on")
        pl.axis("tight")




    def ltspice_tran_parameters(self):
        """
            Syntax: .TRAN <Tstep> <Tstop> [Tstart [dTmax]] [modifiers]
            .TRAN <Tstop> [modifiers]
        """

        with open("%s.%s" % (self.BasePath, self.ASC_Extension), "rb") as f:
            for s in f:
                n = s.find(".tran")
                if n > 0:
                    s = s[n:].split()
                    if len(s) == 2:
                        TStop, x = self.prefix_convert(s[1])
                        TStep = None
                    elif len(s) == 2:
                        TStep, _ = self.prefix_convert(s[0])
                        TStop, x = self.prefix_convert(s[1])
                    else:
                        TStep = None
                        TStop = None
        print("A"*20,x)
        self.TStep = TStep
        self.TStop = TStop
        self.PrefixFactor = x

if __name__ == '__main__':

    import matplotlib.pyplot as pl

    S = LTSpice('LM741', Verbose=1)

    #S.Run()

    S.read_multiple(3)

#    pl.close('all')
#
#    S.plot_channel('V(6)')

    S.Print()