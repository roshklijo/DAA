import tkinter as tk
from tkinter import ttk, messagebox

from algorithms.knapsack import optimize_appliances


class PowerWiseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerWise - Smart Electricity Usage Optimizer")
        self.root.geometry("1150x750")
        self.root.minsize(950, 650)
        self.root.configure(bg="#F3F6FA")

        self.appliances = []
        self.edit_index = None
        self.capacity = 2000
        self.last_result = None

        self.create_header()
        self.create_dashboard()
        self.create_footer()
        self.refresh_appliances()

    def create_header(self):
        header = tk.Frame(self.root, bg="#173B57", height=95)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header, text="⚡ PowerWise",
            font=("Segoe UI", 25, "bold"),
            bg="#173B57", fg="white"
        ).pack(anchor="w", padx=30, pady=(12, 0))

        tk.Label(
            header,
            text="Smart Electricity Usage Optimizer | 0/1 Knapsack",
            font=("Segoe UI", 11),
            bg="#173B57", fg="#D5E6F2"
        ).pack(anchor="w", padx=32)

    def create_dashboard(self):
        main = tk.Frame(self.root, bg="#F3F6FA")
        main.pack(fill="both", expand=True, padx=22, pady=12)

        tk.Label(
            main, text="Energy Optimization Dashboard",
            font=("Segoe UI", 18, "bold"),
            bg="#F3F6FA", fg="#173B57"
        ).pack(anchor="w", pady=(0, 8))

        capacity_frame = tk.Frame(main, bg="#F3F6FA")
        capacity_frame.pack(fill="x", pady=(0, 8))

        tk.Label(
            capacity_frame, text="Maximum Power Capacity (W):",
            font=("Segoe UI", 10, "bold"),
            bg="#F3F6FA", fg="#173B57"
        ).pack(side="left")

        self.capacity_entry = ttk.Entry(capacity_frame, width=14)
        self.capacity_entry.insert(0, "2000")
        self.capacity_entry.pack(side="left", padx=10)

        tk.Button(
            capacity_frame, text="Set Capacity",
            command=self.set_capacity,
            bg="#173B57", fg="white",
            relief="flat", padx=12, pady=5
        ).pack(side="left")

        cards = tk.Frame(main, bg="#F3F6FA")
        cards.pack(fill="x", pady=5)

        self.capacity_card = self.create_card(
            cards, "POWER CAPACITY", "2000 W"
        )
        self.count_card = self.create_card(
            cards, "APPLIANCES", "0"
        )
        self.used_card = self.create_card(
            cards, "POWER USED", "0 W"
        )
        self.priority_card = self.create_card(
            cards, "PRIORITY SCORE", "0"
        )

        content = tk.Frame(main, bg="#F3F6FA")
        content.pack(fill="both", expand=True, pady=(10, 0))

        left = tk.LabelFrame(
            content, text=" Appliance Management ",
            font=("Segoe UI", 11, "bold"),
            bg="white", fg="#173B57",
            padx=10, pady=8
        )
        left.pack(
            side="left", fill="both",
            expand=True, padx=(0, 8)
        )

        right = tk.LabelFrame(
            content, text=" Optimization Results ",
            font=("Segoe UI", 11, "bold"),
            bg="white", fg="#173B57",
            padx=10, pady=8
        )
        right.pack(
            side="right", fill="both",
            expand=True, padx=(8, 0)
        )

        self.create_appliance_form(left)
        self.create_appliance_list(left)
        self.create_results_panel(right)

    def create_card(self, parent, heading, value):
        card = tk.Frame(
            parent, bg="white",
            highlightbackground="#DCE4EC",
            highlightthickness=1,
            padx=12, pady=9
        )
        card.pack(
            side="left", fill="x",
            expand=True, padx=4
        )

        tk.Label(
            card, text=heading,
            font=("Segoe UI", 9, "bold"),
            bg="white", fg="#718096"
        ).pack(anchor="w")

        value_label = tk.Label(
            card, text=value,
            font=("Segoe UI", 18, "bold"),
            bg="white", fg="#173B57"
        )
        value_label.pack(anchor="w", pady=(4, 0))

        return value_label

    def create_appliance_form(self, parent):
        form = tk.Frame(parent, bg="white")
        form.pack(fill="x", pady=4)

        for col, label in enumerate(
            ("Appliance Name", "Power (W)", "Priority")
        ):
            tk.Label(
                form, text=label, bg="white",
                font=("Segoe UI", 9, "bold")
            ).grid(
                row=0, column=col,
                sticky="w", pady=4
            )

        self.name_entry = ttk.Entry(form, width=19)
        self.name_entry.grid(
            row=1, column=0, padx=(0, 5)
        )

        self.power_entry = ttk.Entry(form, width=10)
        self.power_entry.grid(
            row=1, column=1, padx=5
        )

        self.priority_entry = ttk.Entry(form, width=9)
        self.priority_entry.grid(
            row=1, column=2, padx=5
        )

        self.add_button = tk.Button(
            form, text="Add Appliance",
            command=self.add_appliance,
            bg="#173B57", fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat", padx=8, pady=6
        )
        self.add_button.grid(
            row=2, column=0,
            columnspan=3, sticky="ew", pady=8
        )

    def create_appliance_list(self, parent):
        tk.Label(
            parent, text="Appliance List",
            bg="white", fg="#173B57",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", pady=(4, 5))

        columns = ("name", "power", "priority")

        self.tree = ttk.Treeview(
            parent,
            columns=columns,
            show="headings",
            height=5
        )

        self.tree.heading("name", text="Name")
        self.tree.heading("power", text="Power (W)")
        self.tree.heading("priority", text="Priority")

        self.tree.column("name", width=150)
        self.tree.column(
            "power", width=90, anchor="center"
        )
        self.tree.column(
            "priority", width=80, anchor="center"
        )

        self.tree.pack(fill="x", expand=False)

        buttons = tk.Frame(parent, bg="white")
        buttons.pack(fill="x", pady=7)

        tk.Button(
            buttons, text="Edit",
            command=self.edit_appliance,
            bg="#DCE8F2", fg="#173B57",
            relief="flat", padx=18, pady=5
        ).pack(side="left", padx=3)

        tk.Button(
            buttons, text="Delete",
            command=self.delete_appliance,
            bg="#FCE4E4", fg="#A12626",
            relief="flat", padx=18, pady=5
        ).pack(side="left", padx=3)

    def create_results_panel(self, parent):
        self.optimize_button = tk.Button(
            parent,
            text="⚡ Optimize Appliances",
            command=self.optimize,
            bg="#18794E", fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat", padx=12, pady=9
        )
        self.optimize_button.pack(
            side="bottom", fill="x", pady=(5, 0)
        )

        self.steps_button = tk.Button(
            parent,
            text="View DP Steps",
            command=self.show_dp_steps,
            state="disabled",
            bg="#DCE8F2", fg="#173B57",
            font=("Segoe UI", 10, "bold"),
            relief="flat", padx=12, pady=7
        )
        self.steps_button.pack(
            side="bottom", fill="x", pady=(5, 0)
        )

        self.results_text = tk.Text(
            parent,
            height=12,
            wrap="word",
            font=("Segoe UI", 10),
            bg="white",
            fg="#173B57",
            relief="flat",
            state="disabled"
        )
        self.results_text.pack(
            fill="both", expand=True
        )

    def add_appliance(self):
        name = self.name_entry.get().strip()

        try:
            if not name:
                raise ValueError("Enter an appliance name.")

            power = int(self.power_entry.get().strip())
            priority = int(self.priority_entry.get().strip())

            if power <= 0 or priority <= 0:
                raise ValueError(
                    "Power and priority must be positive."
                )

        except ValueError as error:
            messagebox.showerror(
                "Invalid Input", str(error)
            )
            return

        appliance = {
            "name": name,
            "power_w": power,
            "priority": priority
        }

        if self.edit_index is not None:
            self.appliances[self.edit_index] = appliance
            self.edit_index = None
            self.add_button.config(text="Add Appliance")
        else:
            self.appliances.append(appliance)

        self.clear_form()
        self.invalidate_result()
        self.refresh_appliances()

    def edit_appliance(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "Select Appliance",
                "Please select an appliance to edit."
            )
            return

        index = self.tree.index(selection[0])
        appliance = self.appliances[index]

        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, appliance["name"])

        self.power_entry.delete(0, tk.END)
        self.power_entry.insert(
            0, str(appliance["power_w"])
        )

        self.priority_entry.delete(0, tk.END)
        self.priority_entry.insert(
            0, str(appliance["priority"])
        )

        self.edit_index = index
        self.add_button.config(text="Update Appliance")

    def delete_appliance(self):
        selection = self.tree.selection()

        if not selection:
            messagebox.showwarning(
                "Select Appliance",
                "Please select an appliance to delete."
            )
            return

        index = self.tree.index(selection[0])
        del self.appliances[index]

        self.edit_index = None
        self.clear_form()
        self.add_button.config(text="Add Appliance")
        self.invalidate_result()
        self.refresh_appliances()

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.power_entry.delete(0, tk.END)
        self.priority_entry.delete(0, tk.END)

    def invalidate_result(self):
        self.last_result = None
        self.steps_button.config(state="disabled")
        self.used_card.config(text="0 W")
        self.priority_card.config(text="0")

        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.config(state="disabled")

    def set_capacity(self):
        try:
            capacity = int(
                self.capacity_entry.get().strip()
            )

            if capacity < 0:
                raise ValueError

        except ValueError:
            messagebox.showerror(
                "Invalid Capacity",
                "Enter a non-negative whole number."
            )
            return

        self.capacity = capacity
        self.capacity_card.config(
            text=f"{capacity} W"
        )
        self.invalidate_result()

        messagebox.showinfo(
            "Capacity Updated",
            f"Maximum power capacity set to {capacity} W."
        )

    def optimize(self):
        if not self.appliances:
            messagebox.showwarning(
                "No Appliances",
                "Please add at least one appliance first."
            )
            return

        try:
            result = optimize_appliances(
                self.appliances,
                self.capacity
            )
        except ValueError as error:
            messagebox.showerror(
                "Optimization Error", str(error)
            )
            return

        self.last_result = result

        self.used_card.config(
            text=f'{result["total_power"]} W'
        )
        self.priority_card.config(
            text=str(result["total_priority"])
        )

        selected_ids = {
            id(item) for item in result["selected"]
        }

        output = [
            "OPTIMIZATION SUCCESSFUL",
            "",
            f"Available capacity: {self.capacity} W",
            f"Total power used: {result['total_power']} W",
            f"Remaining capacity: {result['remaining_capacity']} W",
            f"Maximum priority: {result['total_priority']}",
            "",
            "SELECTED APPLIANCES"
        ]

        if result["selected"]:
            for item in result["selected"]:
                output.append(
                    f"✓ {item['name']} - {item['power_w']} W "
                    f"(Priority {item['priority']})"
                )
        else:
            output.append(
                "No appliances fit the capacity."
            )

        output.extend(["", "NOT SELECTED"])

        unselected = [
            item for item in self.appliances
            if id(item) not in selected_ids
        ]

        if unselected:
            for item in unselected:
                output.append(f"• {item['name']}")
        else:
            output.append("None")

        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(
            "1.0", "\n".join(output)
        )
        self.results_text.config(state="disabled")

        self.steps_button.config(state="normal")

    def show_dp_steps(self):
        if self.last_result is None:
            messagebox.showwarning(
                "Optimize First",
                "Please optimize the appliances before viewing DP steps."
            )
            return

        dp = self.last_result["dp_table"]

        window = tk.Toplevel(self.root)
        window.title(
            "PowerWise - DP Step Visualization"
        )
        window.geometry("950x650")
        window.minsize(750, 450)
        window.configure(bg="#F3F6FA")

        tk.Label(
            window,
            text="0/1 Knapsack - Dynamic Programming Steps",
            font=("Segoe UI", 17, "bold"),
            bg="#F3F6FA",
            fg="#173B57"
        ).pack(pady=(12, 4))

        tk.Label(
            window,
            text="Use Next Step to see how each appliance is evaluated.",
            font=("Segoe UI", 10),
            bg="#F3F6FA",
            fg="#526477"
        ).pack(pady=(0, 8))

        step_label = tk.Label(
            window,
            text="",
            font=("Segoe UI", 12, "bold"),
            bg="white",
            fg="#173B57",
            padx=12,
            pady=10
        )
        step_label.pack(
            fill="x", padx=15, pady=5
        )

        explanation = tk.Label(
            window,
            text="",
            font=("Segoe UI", 10),
            bg="#F3F6FA",
            fg="#173B57"
        )
        explanation.pack(pady=4)

        table_frame = tk.Frame(
            window, bg="#F3F6FA"
        )
        table_frame.pack(
            fill="both", expand=True,
            padx=15, pady=8
        )

        columns = (
            "capacity",
            "exclude",
            "include",
            "best",
            "decision"
        )

        table = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        headings = {
            "capacity": "Capacity (W)",
            "exclude": "Exclude Value",
            "include": "Include Value",
            "best": "Best DP Value",
            "decision": "Decision"
        }

        widths = {
            "capacity": 120,
            "exclude": 130,
            "include": 130,
            "best": 130,
            "decision": 170
        }

        for column in columns:
            table.heading(
                column, text=headings[column]
            )
            table.column(
                column,
                width=widths[column],
                anchor="center"
            )

        y_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=table.yview
        )

        x_scroll = ttk.Scrollbar(
            window,
            orient="horizontal",
            command=table.xview
        )

        table.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        table.pack(
            side="left", fill="both", expand=True
        )
        y_scroll.pack(side="right", fill="y")
        x_scroll.pack(fill="x", padx=15)

        navigation = tk.Frame(
            window, bg="#F3F6FA"
        )
        navigation.pack(
            fill="x", padx=15, pady=10
        )

        state = {"step": 0}
        total_steps = len(self.appliances)

        def display_step():
            step = state["step"]

            for row in table.get_children():
                table.delete(row)

            if step == 0:
                step_label.config(
                    text="Step 0: Initialization"
                )

                explanation.config(
                    text=(
                        "Every DP table cell is initially "
                        "set to zero."
                    )
                )

                for cap in range(self.capacity + 1):
                    table.insert(
                        "",
                        tk.END,
                        values=(
                            cap,
                            "-",
                            "-",
                            0,
                            "Initialize to 0"
                        )
                    )

            else:
                appliance = self.appliances[step - 1]
                power = appliance["power_w"]
                priority = appliance["priority"]

                step_label.config(
                    text=(
                        f"Step {step} of {total_steps}: "
                        f"{appliance['name']}"
                    )
                )

                explanation.config(
                    text=(
                        f"Power: {power} W | "
                        f"Priority: {priority}. "
                        "Compare excluding and including "
                        "this appliance."
                    )
                )

                previous_row = dp[step - 1]
                current_row = dp[step]

                for cap in range(self.capacity + 1):
                    exclude_value = previous_row[cap]

                    if power <= cap:
                        include_value = (
                            priority
                            + previous_row[cap - power]
                        )

                        decision = (
                            "Include"
                            if include_value > exclude_value
                            else "Skip"
                        )
                    else:
                        include_value = "-"
                        decision = "Skip - does not fit"

                    table.insert(
                        "",
                        tk.END,
                        values=(
                            cap,
                            exclude_value,
                            include_value,
                            current_row[cap],
                            decision
                        )
                    )

            previous_button.config(
                state=(
                    "normal" if step > 0
                    else "disabled"
                )
            )

            next_button.config(
                state=(
                    "normal" if step < total_steps
                    else "disabled"
                )
            )

        def previous_step():
            if state["step"] > 0:
                state["step"] -= 1
                display_step()

        def next_step():
            if state["step"] < total_steps:
                state["step"] += 1
                display_step()

        previous_button = tk.Button(
            navigation,
            text="← Previous Step",
            command=previous_step,
            bg="#DCE8F2",
            fg="#173B57",
            relief="flat",
            padx=15,
            pady=8
        )
        previous_button.pack(side="left")

        next_button = tk.Button(
            navigation,
            text="Next Step →",
            command=next_step,
            bg="#173B57",
            fg="white",
            relief="flat",
            padx=15,
            pady=8
        )
        next_button.pack(side="right")

        display_step()

    def refresh_appliances(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for appliance in self.appliances:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    appliance["name"],
                    appliance["power_w"],
                    appliance["priority"]
                )
            )

        self.count_card.config(
            text=str(len(self.appliances))
        )

    def create_footer(self):
        footer = tk.Frame(
            self.root, bg="#E4EBF2", height=32
        )
        footer.pack(
            side="bottom", fill="x"
        )

        tk.Label(
            footer,
            text="PowerWise | DAA Project | Dynamic Programming",
            font=("Segoe UI", 9),
            bg="#E4EBF2",
            fg="#526477"
        ).pack(pady=7)


def run_app():
    root = tk.Tk()
    PowerWiseApp(root)
    root.mainloop()


if __name__ == "__main__":
    run_app()