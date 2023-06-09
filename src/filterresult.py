import customtkinter
import copy
import src.final as final


class Result(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.final_condition = {"time": [], "loc": [], "dep": []}
        self.final_checkbox = {"cid": False, "loc": False, "tch": False, "t": False}
        # customtkinter.CTkTextbox(master=self, width=250)
        self.frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame.grid(row=0, column=0, padx=20)

        # result area lebel
        self.result_label = customtkinter.CTkLabel(
            master=self.frame, text="Courses available", font=("Arial", 24)
        )
        self.result_label.grid(row=0, column=0, pady=20, padx=20)
        # result textbox
        self.textbox = customtkinter.CTkTextbox(
            master=self.frame,
            width=300,
            height=500,
            font=("Arial", 18),
        )
        self.textbox.grid(
            row=1,
            column=0,
            padx=(20, 20),
            pady=(0, 20),
            sticky="nsew",
        )
        self.textbox.insert("0.0", "No courses available.")

    def rm_null_key(self, raw_condition) -> dict:
        """Remove all keys with value: empty list, making the select function work correctly"""

        for key, val in raw_condition.copy().items():
            if val == [] or val == [""]:
                raw_condition.pop(key)
        return raw_condition

    def change_filtered_result(
        self, filtered_result=None, checkbox_filter=None, strict=False
    ) -> None:
        if filtered_result == None:
            filtered_result = self.final_condition
        if checkbox_filter == None:
            checkbox_filter = self.final_checkbox
        # TODO: complete showing
        for key in self.final_condition.keys():
            try:
                self.final_condition[key] = filtered_result[key]
            except KeyError:
                continue

        for key in self.final_checkbox.keys():
            try:
                self.final_checkbox[key] = checkbox_filter[key]
            except KeyError:
                continue
        # print(checkbox_filter)
        res = final.select(
            self.rm_null_key(copy.deepcopy(self.final_condition)),
            strict=strict,
        )
        self.textbox.delete("0.0", "end")
        """ try:
            # available_courses = res[["課程中文名稱", "教室與上課時間"]].apply("\n  - ".join, axis=1).str.cat(sep="\n")
            available_courses = res["課程中文名稱"].str.cat(sep="\n")
        except:
            available_courses = "No courses available." """
        try:
            available_courses = ""
            CourseIDList = list(res["科號"])
            NameList = list(res["課程中文名稱"])

            tmp = []
            for item in list(res["教室與上課時間"]):
                tmp.append(item.split("\n")[0])
            TimeList = []
            for item in tmp:
                if len(item.split("\t")) > 1:
                    TimeList.append(item.split("\t")[1])
                else:
                    TimeList.append("")

            tmp = [item.split("\n")[0] for item in list(res["教室與上課時間"])]
            LocList = [item.split("\t")[0] for item in tmp]

            tmp = [item.split("\n")[0] for item in list(res["授課教師"])]
            TeacherList = [item.split("\t")[0] for item in tmp]

            for t, name, cid, tch, loc in zip(
                TimeList, NameList, CourseIDList, TeacherList, LocList, strict=True
            ):
                available_courses += (
                    f'{cid if self.final_checkbox["cid"] else ""}'
                    + "\n"
                    + f'{name} {tch if self.final_checkbox["tch"] else ""}'
                    + "\n"
                    + f'{t if self.final_checkbox["t"] else ""}'
                    + f'{loc if self.final_checkbox["loc"] else ""}'
                    + "\n\n"
                )
        except Exception as e:
            available_courses = "No courses available."

        self.textbox.insert("0.0", available_courses)
