from __future__ import absolute_import
# First name : main folder, second name .py file and last : class name
from fretboardgtr.fretboardgtr import FretBoardGtr
import svgwrite


class ChordGtr(FretBoardGtr):

    def __init__(self, fingering=[0, 3, 2, 0, 1, 0], root='C', lefthand=False):
        FretBoardGtr.__init__(self)
        self.fingering = fingering
        self.root = root
        self.lefthand = lefthand

    def emptybox(self):
        self.dwg = svgwrite.Drawing(
            self.path,
            size=(self.wf*(len(self.tuning)+2),
                  self.hf*6+self.hf*(self.gap-3)),
            profile='tiny'
        )

    def background_fill(self):
        self.dwg.add(
            self.dwg.rect(
                insert=(self.wf + self._ol, self.hf + self._ol),
                size=((len(self.tuning)-1)*self.wf, (self.gap+1) *
                      (self.hf)),  # -2 evite case du bas du tuning
                rx=None, ry=None,
                fill=self.background_color
            )
        )

    def background_fill_image(self):
        self.dwg.add(
            self.dwg.image("wood1.jfif",
                           x=self.wf + self._ol,
                           y=self.hf + self._ol,
                           width=(len(self.tuning)-1)*self.wf,
                           # -2 evite case du bas du tuning
                           height=(len(self.tuning)-2)*self.hf,
                           preserveAspectRatio="none",
                           opacity=0.90
                           )
        )

    def add_dot(self):
        dot, nbdot = self.wheredot()
        if self.fingering.max > 4:
            for i in range(len(dot)):
                if nbdot[i] == 1:
                    self.dwg.add(self.dwg.circle(((len(self.tuning)/2+1/2)*self.wf + self._ol, (1.5 +
                                 dot[i])*self.hf+self._ol), r=self.dot_radius, fill=self.dot_color, stroke=self.dot_color_stroke, stroke_width=self.dot_width_stroke))
                if nbdot[i] == 2:
                    self.dwg.add(self.dwg.circle(((len(self.tuning)/2 - 1/2)*self.wf + self._ol, (1.5 +
                                 dot[i])*self.hf+self._ol), r=self.dot_radius, fill=self.dot_color, stroke=self.dot_color_stroke, stroke_width=self.dot_width_stroke))
                    self.dwg.add(self.dwg.circle(((len(self.tuning)/2 + 1.5)*self.wf + self._ol, (1.5 +
                                 dot[i])*self.hf+self._ol), r=self.dot_radius, fill=self.dot_color, stroke=self.dot_color_stroke, stroke_width=self.dot_width_stroke))
        else:
            self.dwg.add(self.dwg.circle(((len(self.tuning)/2+1/2)*self.wf + self._ol, (3.5)*self.hf+self._ol),
                         r=self.dot_radius, fill=self.dot_color, stroke=self.dot_color_stroke, stroke_width=self.dot_width_stroke))

    def createfretboard(self):
        '''
        Create an empty set of rectangles based on tunings.
        '''
        # Creation of fret
        if self.fingering.max > 4:
            for i in range(self.gap+2):
                # self.gap +2 : two is for the beginning and the end of the fretboard
                self.dwg.add(
                    self.dwg.line(
                        start=(self.wf + self._ol, (self.hf)*(i+1)+self._ol),
                        end=((self.wf)*(len(self.tuning)) +
                             self._ol, (self.hf)*(1+i)+self._ol),
                        stroke=self.fretcolor,
                        stroke_width=self.fretsize
                    )
                )
        else:
            for i in range(self.gap+1):
                # self.gap +1 :  for  the end of the fretboard and (i+2) to avoid first fret when nut
                self.dwg.add(
                    self.dwg.line(
                        start=(self.wf + self._ol, (self.hf)*(i+2)+self._ol),
                        end=((self.wf)*(len(self.tuning)) +
                             self._ol, (self.hf)*(i+2)+self._ol),
                        stroke=self.fretcolor,
                        stroke_width=self.fretsize
                    )
                )

        # creation of strings
        if self.string_same_size == False:
            string_size_list = [((self.string_size)-i/4)
                                for i in range(len(self.tuning))]

        elif self.string_same_size == True:
            string_size_list = [(self.string_size)
                                for i in range(len(self.tuning))]

        for i in range(len(self.tuning)):

            self.dwg.add(
                self.dwg.line(
                    start=((self.wf)*(1+i)+self._ol,
                           self.hf+self._ol-self.fretsize/2),
                    end=((self.wf)*(1+i)+self._ol, self.hf+self._ol +
                         (self.gap+1)*self.hf + self.fretsize/2),
                    stroke=self.strings_color,
                    stroke_width=string_size_list[i]
                )
            )

    def nut(self):
        '''
        Create nut if condition in fillfretboard.

        '''
        if self.string_same_size == False:
            self.dwg.add(
                self.dwg.line(
                    start=(self.wf + self._ol-((self.string_size)) /
                           2, (self.hf)*(1)+self._ol),
                    end=((self.wf)*(len(self.tuning))+self._ol +
                         ((self.string_size)-len(self.tuning)/4)/2, (self.hf)*(1)+self._ol),
                    stroke=self.nut_color,
                    stroke_width=self.nut_height
                )
            )
        else:
            self.dwg.add(
                self.dwg.line(
                    start=(self.wf + self._ol-((self.string_size)) /
                           2, (self.hf)*(1)+self._ol),
                    end=((self.wf)*(len(self.tuning))+self._ol +
                         ((self.string_size))/2, (self.hf)*(1)+self._ol),
                    stroke=self.nut_color,
                    stroke_width=self.nut_height
                )
            )

    def show_tuning(self):
        '''
        Show  tuning at the end of the neck.
        '''
        if self.fingering.max > 4:
            for i in range(len(self.tuning)):
                X = self.wf*(1+i)+self._ol
                Y = self.hf*(self.fingering.max+1/2+1)+self._ol

                t = svgwrite.text.Text(self.tuning[i], insert=(X, Y), dy=[
                                       "0.3em"], font_size=self.fontsize_bottom_tuning, font_weight="normal", style="text-anchor:middle")
                self.dwg.add(t)

        else:
            for i in range(len(self.tuning)):
                X = self.wf*(1+i)+self._ol
                Y = self.hf*(5+1/2)+self._ol

                t = svgwrite.text.Text(self.tuning[i], insert=(X, Y), dy=[
                                       "0.3em"], font_size=self.fontsize_bottom_tuning, font_weight="normal", style="text-anchor:middle")
                self.dwg.add(t)

    def fillfretboard(self):

        if self.lefthand:
            self.fingering = self.fingering.reverse()
            self.tuning = self.tuning[::-1]
        self.dist()  # modify self.gap

        note_names = self.notesname()
        intervals = FretBoardGtr.find_intervals(note_names, self.root)

        if self.fingering.max > 4:
            # print the number to the right of the minfret

            X = self.wf*(1+len(self.tuning))+self._ol
            Y = self.hf*(3/2)+self._ol
            t = svgwrite.text.Text(str(self.fingering.min), insert=(X, Y), dy=[
                                   "0.3em"], font_size=self.fontsize_fret, font_weight="bold", style="text-anchor:middle")
            self.dwg.add(t)

            strings_and_frets = self.fingering.offset(self.fingering.min)

        else:
            self.nut()
            strings_and_frets = self.fingering

        for (string, fret), note_name, interval in\
            zip(strings_and_frets, note_names, intervals):

            if fret is None:
                X = self.wf*(1+string)+self._ol
                Y = self.hf*(1/2)+self._ol

                t = svgwrite.text.Text('X', insert=(X, Y), dy=[
                                       "0.3em"], font_size=self.fontsize_cross, font_weight="bold", fill=self.cross_color, style="text-anchor:middle")
                self.dwg.add(t)
                #dwg.add(dwg.image("cross.svg",x=(i+1-0.3)*self.wf +self._ol,y=self.hf*(1/4-0.2)+self._ol,width=2*self.R))

            else:
                X = self.wf*(1+string)+self._ol
                Y = self.hf*(fret+1/2)+self._ol

                if fret == 0:
                    if self.open_color_chord:
                        color = self.dic_color[interval]
                    else:
                        color = self.fretted_circle_color
                    if self.show_note_name:
                        name_text = note_name
                    elif self.show_degree_name:
                        name_text = str(interval)
                    else:
                        name_text = ""
                    self.dwg.add(self.dwg.circle((X, Y), r=self.R, fill=self.open_circle_color,
                                 stroke=color, stroke_width=self.open_circle_stroke_width))
                    t = svgwrite.text.Text(name_text, insert=(X, Y), dy=[
                                           "0.3em"], font_size=self.fontsize_text, font_weight="bold", fill=self.open_text_color, style="text-anchor:middle")
                    self.dwg.add(t)
                else:
                    if self.color_chord:
                        color = self.dic_color[interval]
                    else:
                        color = self.fretted_circle_color
                    if self.show_note_name:
                        name_text = note_name
                    elif self.show_degree_name:
                        name_text = str(interval)
                    else:
                        name_text = ""

                    self.dwg.add(self.dwg.circle((X, Y), r=self.R, fill=color,
                                 stroke=self.fretted_circle_stroke_color, stroke_width=self.fretted_circle_stroke_width))
                    t = svgwrite.text.Text(name_text, insert=(X, Y), dy=[
                                           "0.3em"], font_size=self.fontsize_text, fill=self.fretted_text_color, font_weight="bold", style="text-anchor:middle")
                    self.dwg.add(t)

            if self.show_tun:
                self.show_tuning()

    def draw(self):
        self.dist()
        self.emptybox()
        self.background_fill()
        # self.background_fill_image()
        self.add_dot()
        self.createfretboard()
        self.fillfretboard()

        return self.dwg
