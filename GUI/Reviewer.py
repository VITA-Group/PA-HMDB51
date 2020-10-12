import cv2, json, os, argparse
import numpy as np 
import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import PIL.Image, PIL.ImageTk


class MyVideoCapture(object):
    def __init__(self, path=0):
        self.vid = cv2.VideoCapture(path)
        self.frames = list()
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", path)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.current_frame = 0
        self._get_frame()

    def get_frame(self, n):
        if n < len(self.frames):
            return True, self.frames[n], n
        else:
            return False, None, None

    def _get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            while ret:
                self.frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                ret, frame = self.vid.read()

    def get_previous_frame(self):
        if self.current_frame:
            self.current_frame -= 1
            return True, self.frames[self.current_frame], self.current_frame
        else:
            return False, None, None

    def get_next_frame(self):
        if self.current_frame + 1 < len(self.frames):
            self.current_frame += 1
            return True, self.frames[self.current_frame], self.current_frame
        else:
            return False, None, None

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


class Reviewer:
    def __init__(self, master, hmdb51_video_root_dir, PA_label_root_dir):
        self.master = master
        self.master.title = "Frame review"
        
        # dirs:
        self.hmdb51_video_root_dir = hmdb51_video_root_dir # 'D:\hmdb51_org'
        self.PA_label_root_dir = PA_label_root_dir # 'D:\HMDB51_PrivacyAttributes'
        self.list_folders = [f for f in os.listdir(self.hmdb51_video_root_dir) if len(f.split(".")) == 1]

        self.list_frames = None
        self.list_vids_not_review = None
        self.list_vids_reviewed = None
        
        self.current_vid = None
        self.meta_data = None
        self.vid = None
        self.canvas_vid = None
        
        self.vid_scences = None
        self.start_frame = None
        self.end_frame = None
        self.runner_frame = None
        self.note = None
        self.scroll = None
        self.var_start_text = StringVar()
        self.current_frame = StringVar()
        self.bool_start = False
        self.bool_get_previous = False
        self.bool_get_next = True

        # TKinter variables:
        self.current_folder = StringVar()
        self.current_vid_review = StringVar()
        self.current_vid_not_review = StringVar()
        
        # set tracing for Tkinter variables:
        self.current_folder.set(NONE)
        self.current_folder.trace('w', self.current_folder_trace)
        self.current_vid_review.set(NONE)
        self.current_vid_review.trace('w', self.current_vid_review_trace)
        self.current_vid_not_review.set(NONE)
        self.current_vid_not_review.trace('w', self.current_vid_not_review_trace)
        

        # privacy attributes
        self.attributes = {
            "gender": [StringVar(), ["Unidentifiable", "M", "F", "M & F"]],
            "face": [StringVar(), ["Invisible", "Partially visible", "Completely visible"]],
            "skin_color": [StringVar(), ["Unidentifiable", "W", "Y", "B", "W & Y", "W & B", "Y & B", "All"]],
            "nudity": [StringVar(), ["No-nudity", "Partial-nudity", "Semi-nudity"]],
            "relationship": [StringVar(), ["Unidentifiable", "Identifiable"]]
        }
        
        ## Define GUI layout
        # LabelFrames:
        self.video_widget = LabelFrame(self.master) # shows videos
        self.video_widget.grid(row=0, column=0)
        self.video_ctrl_widget = LabelFrame(self.master) # video control: previous/next frame
        self.video_ctrl_widget.grid(row=1, column=0)
        self.video_menu_widget = LabelFrame(self.master) # dropdown menu for video selection
        self.video_menu_widget.grid(row=2)
        self.annotation_widget = LabelFrame(self.master) # show privacy attribute annotations
        self.annotation_widget.grid(row=0, column=1)
        self.comment_widget = LabelFrame(self.master) # reviewers can add comments here
        self.comment_widget.grid(row=1, column=1)

        # Video control widget:
        self.bnt_start = Button(self.video_ctrl_widget, textvariable=self.var_start_text, width=13, command=self.start_stop) # start Button
        self.bnt_start.grid(row=1, column=0, )
        self.bnt_prev = Button(self.video_ctrl_widget, text="previous frame", width=12, command=self.get_previous_frame) # previous button
        self.bnt_prev.grid(row=1, column=0, sticky=W)
        self.bnt_next = Button(self.video_ctrl_widget, text="next frame", width=12, command=self.get_next_frame) # next button
        self.bnt_next.grid(row=1, column=0, sticky=E)
        self.bnt_restart = Button(self.video_ctrl_widget, text="restart", width=50, command=self.restart) # restart button
        self.bnt_restart.grid(row=2)

        # Video menu widget:
        Label(self.video_menu_widget, text="Actions").grid(row=0, column=0)
        Label(self.video_menu_widget, text="To be Reviewed").grid(row=0, column=1)
        Label(self.video_menu_widget, text="Reviewed").grid(row=0, column=2)
        self.menu_folders = OptionMenu(self.video_menu_widget, self.current_folder, *self.list_folders if self.list_folders else [None])
        self.menu_folders.grid(row=1, column=0)
        self.menu_frames_not_review = OptionMenu(self.video_menu_widget, self.current_vid_not_review, None)
        self.menu_frames_not_review.grid(row=1, column=1)
        self.menu_frames_reviewed = OptionMenu(self.video_menu_widget, self.current_vid_review, None)
        self.menu_frames_reviewed.grid(row=1, column=2)

        # Annotation widget:
        Label(self.annotation_widget, text="current frame:").grid(row=0, sticky=W)
        Label(self.annotation_widget, textvariable=self.current_frame).grid(row=0, padx=85, sticky=E)
        for i, attribute in enumerate(self.attributes):
            Label(self.annotation_widget, text=attribute + ":").grid(row=i + 1, column=0, sticky=W)
            Label(self.annotation_widget, textvariable=self.attributes[attribute][0]).grid(row=i + 1, padx=85, sticky=E)

        # Comment widget:
        Button(self.comment_widget, text="video is ready", command=self.ready, width=15).grid(row=1, column=1)
        Button(self.comment_widget, text="video is not ready", command=self.not_ready, width=15).grid(row=1)
        if self.meta_data and self.current_vid:
            if "note" in self.meta_data[self.current_vid]:
                self.note = self.meta_data[self.current_vid]['note']
            else:
                self.meta_data[self.current_vid]['note'] = None
        self.scroll = ScrolledText(self.comment_widget, width=25, height=5)
        self.scroll.grid(row=0)
        if self.note:
            self.scroll.insert(self.note)
        Button(self.comment_widget, text="Submit", command=self.save_note).grid(row=0, column=1)
        ## End of defining GUI layout

        # update:
        self.update()
        
    ## Video control functions
    def start_stop(self):
        if self.bool_start:
            self._stop()
        else:
            self._start()

    def _start(self):
        self.var_start_text.set("stop")
        self.bool_start = True

    def _stop(self):
        self.var_start_text.set("start")
        self.bool_start = False

    def get_previous_frame(self):
        self.bool_get_previous = True
        self._stop()

    def get_next_frame(self):
        self.bool_get_next = True
        self._stop()

    def restart(self):
        if self.vid:
            self.runner_frame = self.start_frame
            self._start()
       
    # Trace variable functions
    def current_folder_trace(self, *args):
        self.list_frames = list()
        json_files = [f for f in os.listdir(self.PA_label_root_dir) if f.endswith(".json")]
        f = self.current_folder.get() + ".json"
        json_file = f if f in json_files else None
        print(self.PA_label_root_dir, json_files)
        self.list_vids_not_review = list()
        self.list_vids_reviewed = list()
        if json_file:
            json_file_path = os.path.join(self.PA_label_root_dir, json_file)
            with open(json_file_path) as f:
                self.meta_data = json.load(f)
            self.vid_scences = dict()
            # print(self.meta_data)
            for vid in self.meta_data:
                if 'review' in self.meta_data[vid]:
                    if self.meta_data[vid]['review']:
                        self.list_vids_reviewed.append(vid)
                    else:
                        self.list_vids_not_review.append(vid)
                else:
                    self.meta_data[vid]['review'] = False
                    self.list_vids_not_review.append(vid)
        if self.canvas_vid:
            self.vid = None
            self.canvas_vid.destroy()
        self.menu_frames_not_review.destroy()
        self.menu_frames_reviewed.destroy()
        self.current_vid_review.set(NONE)
        self.current_vid_not_review.set(NONE)
        self.menu_frames_reviewed = OptionMenu(self.video_menu_widget, self.current_vid_review,
                                               *self.list_vids_reviewed if len(self.list_vids_reviewed) else [None])
        self.menu_frames_reviewed.grid(row=1, column=2)
        self.menu_frames_not_review = OptionMenu(self.video_menu_widget, self.current_vid_not_review,
                                                 *self.list_vids_not_review if len(self.list_vids_not_review) else [
                                                     None])
        self.menu_frames_not_review.grid(row=1, column=1)

    def current_vid_not_review_trace(self, *args):
        if self.current_vid_not_review.get() != "None" and self.current_vid_not_review.get().lower() != "none" and self.current_vid_not_review.get() != NONE:
            self.current_vid_review.set(None)
            self.current_vid = vid_name = self.current_vid_not_review.get()
            vid_path = self.hmdb51_video_root_dir + "/" + self.current_folder.get() + "/" + vid_name
            if self.vid:
                self.vid.__del__()
            self.vid = MyVideoCapture(vid_path)
            self.start_frame = 0
            self.end_frame = len(self.vid.frames)
            self.runner_frame = self.start_frame
            self.canvas_vid = Canvas(self.video_widget, width=self.vid.width, height=self.vid.height)
            self.canvas_vid.grid(row=0, sticky=W)
            self._start()
            if 'note' in self.meta_data[vid_name]:
                self.scroll.delete('1.0', END)
                self.scroll.insert(INSERT, self.meta_data[vid_name]['note'])
            else:
                self.scroll.delete('1.0', END)

    def current_vid_review_trace(self, *args):
        if self.current_vid_review.get() != "None" and self.current_vid_review.get() != "none" and self.current_vid_review.get() != NONE:
            self.current_vid_not_review.set(None)
            self.current_vid = vid_name = self.current_vid_review.get()
            vid_path = self.hmdb51_video_root_dir + "/" + self.current_folder.get() + "/" + vid_name
            if self.vid:
                self.vid.__del__()
            self.vid = MyVideoCapture(vid_path)
            self.start_frame = 0
            self.end_frame = len(self.vid.frames) -1
            self.runner_frame = self.start_frame
            self.canvas_vid = Canvas(self.video_widget, width=self.vid.width, height=self.vid.height)
            self.canvas_vid.grid(row=0, sticky=W)
            self._start()
            if 'note' in self.meta_data[vid_name] and self.meta_data[vid_name]['note']:
                self.scroll.delete('1.0', END)
                self.scroll.insert(INSERT, self.meta_data[vid_name]['note'])
            else:
                self.scroll.delete('1.0', END)

    # Update functions
    def update(self):
        # print(self.vid,self.runner_frame, self.bool_start)
        if self.vid:
            if self.bool_start or self.bool_get_previous or self.bool_get_next:
                if self.bool_get_previous and self.runner_frame > 0:
                    self.runner_frame -= 1
                    self.bool_get_previous = False
                elif self.bool_get_next and self.runner_frame < self.end_frame:
                    self.runner_frame += 1
                    self.bool_get_next = False
                else:
                    if self.runner_frame < self.end_frame:
                        self.runner_frame += 1
                ret, frame, n = self.vid.get_frame(self.runner_frame)
                if ret:
                    self.annotation_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
                    self.canvas_vid.create_image(0, 0, image=self.annotation_photo, anchor=NW)
                    self.frame_annotation_init_update()
                    self.current_frame.set(str(self.runner_frame))
        self.master.after(15, self.update)
        
    def frame_annotation_init_update(self):
        for i, attribute in enumerate(self.attributes):
            score = -1
            for scene in self.meta_data[self.current_vid][attribute]:
                start = scene[0]
                end = scene[1]
                if self.runner_frame >= start and self.runner_frame <= end:
                    score = scene[2]
                    if isinstance(score, list):
                        if attribute == 'gender':
                            # the only possiblity is score=[1,2] (M & F)
                            score = 3
                        elif attribute == 'skin_color':
                            # [1,2] -> sum([1,2]) + 1 = 4
                            # [1,3] -> sum([1,3]) + 1 = 5
                            # [2,3] -> sum([2,3]) + 1 = 6
                            # [1,2,3] -> sum([1,2,3]) + 1 = 7
                            assert len(score) > 1, "race attribute cannot be %s" % score 
                            assert len(score) <= 3, "race attribute cannot be %s" % score 
                            score = np.sum(score) + 1
                        else:
                            raise Exception('%s is not allowed to have multiple labels' % attribute)
                    break
            if score > -1:
                score = self.attributes[attribute][1][score]
                if self.attributes[attribute][0].get() != score:
                    self.attributes[attribute][0].set(score)
            else:
                self.attributes[attribute][0].set('N/A')
        
    # Check and ddd comments functions
    def save_note(self):
        if self.current_vid:
            self.meta_data[self.current_vid]['note'] = self.scroll.get("1.0", "end-1c")
            self.save_json()

    def ready(self):
        if self.current_vid:
            if self.list_vids_not_review and self.current_vid not in self.list_vids_reviewed:
                self.list_vids_not_review.remove(self.current_vid)
                self.list_vids_reviewed.append(self.current_vid)
                self.current_vid_review.set(self.current_vid)
                self.meta_data[self.current_vid]['review'] = True
                self.menu_frames_not_review.destroy()
                self.menu_frames_reviewed.destroy()
                self.menu_frames_reviewed = OptionMenu(self.video_menu_widget, self.current_vid_review,
                                                       *self.list_vids_reviewed if len(self.list_vids_reviewed) else [
                                                           None])
                self.menu_frames_reviewed.grid(row=1, column=2)
                self.menu_frames_not_review = OptionMenu(self.video_menu_widget, self.current_vid_not_review,
                                                         *self.list_vids_not_review if len(
                                                             self.list_vids_not_review) else [None])
                self.menu_frames_not_review.grid(row=1, column=1)
                self.save_json()

    def not_ready(self):
        if self.current_vid:
            if self.list_vids_reviewed and self.current_vid not in self.list_vids_not_review:
                self.list_vids_reviewed.remove(self.current_vid)
                self.list_vids_not_review.append(self.current_vid)
                self.current_vid_not_review.set(self.current_vid)
                self.meta_data[self.current_vid]['review'] = False
                self.menu_frames_reviewed.destroy()
                self.menu_frames_not_review.destroy()
                self.menu_frames_reviewed = OptionMenu(self.video_menu_widget, self.current_vid_review,
                                                       *self.list_vids_reviewed if len(self.list_vids_reviewed) else [
                                                           None])
                self.menu_frames_reviewed.grid(row=1, column=2)
                self.menu_frames_not_review = OptionMenu(self.video_menu_widget, self.current_vid_not_review,
                                                         *self.list_vids_not_review if len(
                                                             self.list_vids_not_review) else [None])
                self.menu_frames_not_review.grid(row=1, column=1)
                self.save_json()
   
    # save annotations as json files
    def save_json(self):
        if self.meta_data:
            json_str = json.dumps(self.meta_data, indent=4)
            path = os.path.join(self.PA_label_root_dir, self.current_folder.get() + ".json")
            f = open(path, "w")
            f.write(json_str)
            f.close()

if __name__ == '__main__':
    # argparser
    parser= argparse.ArgumentParser()
    parser.add_argument('--hmdb51_video_root_dir', '--vd', default='D:\hmdb51_org', help='root dir for the original HMDB51 dataset')
    parser.add_argument('--PA_label_root_dir', '-pd', default='D:\HMDB51_PrivacyAttributes', help='root dir for privacy attribute labels (stored in JSON files)')
    args = parser.parse_args()

    root = tk.Tk() 
    Reviewer(master = root, hmdb51_video_root_dir = args.hmdb51_video_root_dir, PA_label_root_dir = args.PA_label_root_dir)
    tk.mainloop()
