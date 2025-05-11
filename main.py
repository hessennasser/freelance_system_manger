import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta
import re
import hashlib
import configparser
import os

class FreelancePlatformApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Freelance Platform")
        self.root.geometry("1000x700")
        
        # Database connection
        self.connection = None
        self.cursor = None
        
        # Current user info
        self.current_user = None
        
        # Setup UI
        self.setup_ui()
        
        # Try to connect to database
        self.connect_to_database()
        
    def setup_ui(self):
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Login Frame
        self.login_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.login_frame, text="Login/Register")
        
        # Projects Frame
        self.projects_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.projects_frame, text="Projects")
        
        # Profile Frame
        self.profile_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.profile_frame, text="Profile")
        
        # Messages Frame
        self.messages_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.messages_frame, text="Messages")
        
        # Contracts Frame
        self.contracts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.contracts_frame, text="Contracts")
        
        # Setup each tab
        self.setup_login_tab()
        # Other tabs will be populated after login
        
        # Disable all tabs except login initially
        self.notebook.tab(1, state="disabled")
        self.notebook.tab(2, state="disabled")
        self.notebook.tab(3, state="disabled")
        self.notebook.tab(4, state="disabled")
        
    def setup_login_tab(self):
        # Login section
        login_label = ttk.Label(self.login_frame, text="Login", font=("Arial", 16, "bold"))
        login_label.grid(row=0, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        
        ttk.Label(self.login_frame, text="Email:").grid(row=1, column=0, pady=5, padx=20, sticky="w")
        self.login_email = ttk.Entry(self.login_frame, width=30)
        self.login_email.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(self.login_frame, text="Password:").grid(row=2, column=0, pady=5, padx=20, sticky="w")
        self.login_password = ttk.Entry(self.login_frame, width=30, show="*")
        self.login_password.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        
        login_button = ttk.Button(self.login_frame, text="Login", command=self.login)
        login_button.grid(row=3, column=1, pady=15, padx=5, sticky="w")
        
        # Registration section
        register_label = ttk.Label(self.login_frame, text="Register", font=("Arial", 16, "bold"))
        register_label.grid(row=4, column=0, columnspan=2, pady=10, padx=20, sticky="w")
        
        ttk.Label(self.login_frame, text="Email:").grid(row=5, column=0, pady=5, padx=20, sticky="w")
        self.reg_email = ttk.Entry(self.login_frame, width=30)
        self.reg_email.grid(row=5, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(self.login_frame, text="Password:").grid(row=6, column=0, pady=5, padx=20, sticky="w")
        self.reg_password = ttk.Entry(self.login_frame, width=30, show="*")
        self.reg_password.grid(row=6, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(self.login_frame, text="First Name:").grid(row=7, column=0, pady=5, padx=20, sticky="w")
        self.reg_first_name = ttk.Entry(self.login_frame, width=30)
        self.reg_first_name.grid(row=7, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(self.login_frame, text="Last Name:").grid(row=8, column=0, pady=5, padx=20, sticky="w")
        self.reg_last_name = ttk.Entry(self.login_frame, width=30)
        self.reg_last_name.grid(row=8, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(self.login_frame, text="Role:").grid(row=9, column=0, pady=5, padx=20, sticky="w")
        self.reg_role = ttk.Combobox(self.login_frame, values=["client", "freelancer"], state="readonly", width=27)
        self.reg_role.grid(row=9, column=1, pady=5, padx=5, sticky="w")
        self.reg_role.current(0)
        
        register_button = ttk.Button(self.login_frame, text="Register", command=self.register)
        register_button.grid(row=10, column=1, pady=15, padx=5, sticky="w")
        
    def setup_projects_tab(self):
        # Clear existing widgets
        for widget in self.projects_frame.winfo_children():
            widget.destroy()
            
        # Create project section for clients
        if self.current_user["role"] == "client":
            create_project_frame = ttk.LabelFrame(self.projects_frame, text="Create New Project")
            create_project_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(create_project_frame, text="Title:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
            self.project_title = ttk.Entry(create_project_frame, width=40)
            self.project_title.grid(row=0, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(create_project_frame, text="Description:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
            self.project_desc = tk.Text(create_project_frame, width=50, height=5)
            self.project_desc.grid(row=1, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(create_project_frame, text="Budget Min ($):").grid(row=2, column=0, pady=5, padx=5, sticky="w")
            self.project_budget_min = ttk.Entry(create_project_frame, width=15)
            self.project_budget_min.grid(row=2, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(create_project_frame, text="Budget Max ($):").grid(row=3, column=0, pady=5, padx=5, sticky="w")
            self.project_budget_max = ttk.Entry(create_project_frame, width=15)
            self.project_budget_max.grid(row=3, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(create_project_frame, text="Skills Required:").grid(row=4, column=0, pady=5, padx=5, sticky="w")
            self.project_skills = ttk.Entry(create_project_frame, width=40)
            self.project_skills.grid(row=4, column=1, pady=5, padx=5, sticky="w")
            
            create_button = ttk.Button(create_project_frame, text="Create Project", command=self.create_project)
            create_button.grid(row=5, column=1, pady=10, padx=5, sticky="w")
        
        # Projects listing section
        projects_list_frame = ttk.LabelFrame(self.projects_frame, text="Projects List")
        projects_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create treeview for projects
        columns = ("id", "title", "client", "budget", "status", "created_at")
        self.projects_tree = ttk.Treeview(projects_list_frame, columns=columns, show="headings")
        
        # Define headings
        self.projects_tree.heading("id", text="ID")
        self.projects_tree.heading("title", text="Title")
        self.projects_tree.heading("client", text="Client")
        self.projects_tree.heading("budget", text="Budget")
        self.projects_tree.heading("status", text="Status")
        self.projects_tree.heading("created_at", text="Created At")
        
        # Define columns
        self.projects_tree.column("id", width=50)
        self.projects_tree.column("title", width=200)
        self.projects_tree.column("client", width=150)
        self.projects_tree.column("budget", width=100)
        self.projects_tree.column("status", width=100)
        self.projects_tree.column("created_at", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(projects_list_frame, orient=tk.VERTICAL, command=self.projects_tree.yview)
        self.projects_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.projects_tree.pack(fill="both", expand=True)
        
        # Button frame
        button_frame = ttk.Frame(projects_list_frame)
        button_frame.pack(fill="x", pady=5)
        
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.load_projects)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        view_button = ttk.Button(button_frame, text="View Details", command=self.view_project_details)
        view_button.pack(side=tk.LEFT, padx=5)
        
        # Different buttons based on user role
        if self.current_user["role"] == "freelancer":
            bid_button = ttk.Button(button_frame, text="Place Bid", command=self.place_bid)
            bid_button.pack(side=tk.LEFT, padx=5)
        elif self.current_user["role"] == "client":
            manage_button = ttk.Button(button_frame, text="Manage Project", command=self.manage_project)
            manage_button.pack(side=tk.LEFT, padx=5)
        
        # Load projects
        self.load_projects()
    
    def setup_profile_tab(self):
        # Clear existing widgets
        for widget in self.profile_frame.winfo_children():
            widget.destroy()
            
        profile_info_frame = ttk.LabelFrame(self.profile_frame, text="Profile Information")
        profile_info_frame.pack(fill="x", padx=10, pady=10)
        
        # Basic user info
        ttk.Label(profile_info_frame, text="Email:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.profile_email = ttk.Entry(profile_info_frame, width=40)
        self.profile_email.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        self.profile_email.insert(0, self.current_user["email"])
        self.profile_email.configure(state="readonly")
        
        ttk.Label(profile_info_frame, text="First Name:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.profile_first_name = ttk.Entry(profile_info_frame, width=40)
        self.profile_first_name.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        self.profile_first_name.insert(0, self.current_user["first_name"])
        
        ttk.Label(profile_info_frame, text="Last Name:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.profile_last_name = ttk.Entry(profile_info_frame, width=40)
        self.profile_last_name.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        self.profile_last_name.insert(0, self.current_user["last_name"])
        
        ttk.Label(profile_info_frame, text="Bio:").grid(row=3, column=0, pady=5, padx=5, sticky="w")
        self.profile_bio = tk.Text(profile_info_frame, width=50, height=4)
        self.profile_bio.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        if self.current_user["bio"]:
            self.profile_bio.insert("1.0", self.current_user["bio"])
        
        # Role-specific profile info
        if self.current_user["role"] == "freelancer":
            # Fetch user profile data
            self.cursor.execute("""
                SELECT * FROM user_profiles WHERE user_id = %s
            """, (self.current_user["id"],))
            
            profile_data = self.cursor.fetchone()
            
            freelancer_frame = ttk.LabelFrame(self.profile_frame, text="Freelancer Information")
            freelancer_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(freelancer_frame, text="Headline:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
            self.profile_headline = ttk.Entry(freelancer_frame, width=40)
            self.profile_headline.grid(row=0, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(freelancer_frame, text="Hourly Rate ($):").grid(row=1, column=0, pady=5, padx=5, sticky="w")
            self.profile_hourly_rate = ttk.Entry(freelancer_frame, width=15)
            self.profile_hourly_rate.grid(row=1, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(freelancer_frame, text="Skills:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
            self.profile_skills = ttk.Entry(freelancer_frame, width=40)
            self.profile_skills.grid(row=2, column=1, pady=5, padx=5, sticky="w")
            
            # If profile data exists, populate fields
            if profile_data:
                if profile_data["headline"]:
                    self.profile_headline.insert(0, profile_data["headline"])
                if profile_data["hourly_rate"]:
                    self.profile_hourly_rate.insert(0, str(profile_data["hourly_rate"]))
                if profile_data["skills"]:
                    self.profile_skills.insert(0, profile_data["skills"])
                
                avg_rating_text = f"Average Rating: {profile_data['avg_rating'] if profile_data['avg_rating'] else 'No ratings'}"
                ttk.Label(freelancer_frame, text=avg_rating_text).grid(row=3, column=0, columnspan=2, pady=5, padx=5, sticky="w")
        
        elif self.current_user["role"] == "client":
            # Fetch user profile data
            self.cursor.execute("""
                SELECT * FROM user_profiles WHERE user_id = %s
            """, (self.current_user["id"],))
            
            profile_data = self.cursor.fetchone()
            
            client_frame = ttk.LabelFrame(self.profile_frame, text="Client Information")
            client_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(client_frame, text="Company Name:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
            self.profile_company = ttk.Entry(client_frame, width=40)
            self.profile_company.grid(row=0, column=1, pady=5, padx=5, sticky="w")
            
            # If profile data exists, populate fields
            if profile_data and profile_data["company_name"]:
                self.profile_company.insert(0, profile_data["company_name"])
                
                avg_rating_text = f"Average Rating: {profile_data['avg_rating'] if profile_data['avg_rating'] else 'No ratings'}"
                ttk.Label(client_frame, text=avg_rating_text).grid(row=1, column=0, columnspan=2, pady=5, padx=5, sticky="w")
        
        # Save button
        save_button = ttk.Button(self.profile_frame, text="Save Profile", command=self.save_profile)
        save_button.pack(pady=10)
        
    def setup_messages_tab(self):
        # Clear existing widgets
        for widget in self.messages_frame.winfo_children():
            widget.destroy()
            
        # Split frame into two parts
        left_frame = ttk.Frame(self.messages_frame)
        left_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=5, pady=5)
        
        right_frame = ttk.Frame(self.messages_frame)
        right_frame.pack(side=tk.RIGHT, fill="both", expand=True, padx=5, pady=5)
        
        # Conversations list
        conversations_frame = ttk.LabelFrame(left_frame, text="Conversations")
        conversations_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        columns = ("user_id", "name", "unread")
        self.conversations_tree = ttk.Treeview(conversations_frame, columns=columns, show="headings")
        
        self.conversations_tree.heading("user_id", text="ID")
        self.conversations_tree.heading("name", text="User")
        self.conversations_tree.heading("unread", text="Unread")
        
        self.conversations_tree.column("user_id", width=50)
        self.conversations_tree.column("name", width=150)
        self.conversations_tree.column("unread", width=70)
        
        scrollbar = ttk.Scrollbar(conversations_frame, orient=tk.VERTICAL, command=self.conversations_tree.yview)
        self.conversations_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.conversations_tree.pack(fill="both", expand=True)
        
        refresh_button = ttk.Button(left_frame, text="Refresh", command=self.load_conversations)
        refresh_button.pack(pady=5)
        
        new_message_button = ttk.Button(left_frame, text="New Message", command=self.new_message)
        new_message_button.pack(pady=5)
        
        # Message display area
        messages_display_frame = ttk.LabelFrame(right_frame, text="Messages")
        messages_display_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.messages_text = tk.Text(messages_display_frame, wrap=tk.WORD, state=tk.DISABLED)
        self.messages_text.pack(fill="both", expand=True)
        
        # Message input area
        message_input_frame = ttk.Frame(right_frame)
        message_input_frame.pack(fill="x", padx=5, pady=5)
        
        self.message_entry = tk.Text(message_input_frame, height=3)
        self.message_entry.pack(side=tk.LEFT, fill="x", expand=True)
        
        send_button = ttk.Button(message_input_frame, text="Send", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=5)
        
        # Bind conversation selection
        self.conversations_tree.bind("<<TreeviewSelect>>", self.load_conversation_messages)
        
        # Load conversations
        self.load_conversations()
    
    def setup_contracts_tab(self):
        # Clear existing widgets
        for widget in self.contracts_frame.winfo_children():
            widget.destroy()
            
        # Contracts list
        contracts_list_frame = ttk.LabelFrame(self.contracts_frame, text="Your Contracts")
        contracts_list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        columns = ("id", "title", "with_user", "amount", "start_date", "end_date", "status")
        self.contracts_tree = ttk.Treeview(contracts_list_frame, columns=columns, show="headings")
        
        self.contracts_tree.heading("id", text="ID")
        self.contracts_tree.heading("title", text="Title")
        self.contracts_tree.heading("with_user", text="With")
        self.contracts_tree.heading("amount", text="Amount")
        self.contracts_tree.heading("start_date", text="Start Date")
        self.contracts_tree.heading("end_date", text="End Date")
        self.contracts_tree.heading("status", text="Status")
        
        self.contracts_tree.column("id", width=50)
        self.contracts_tree.column("title", width=200)
        self.contracts_tree.column("with_user", width=150)
        self.contracts_tree.column("amount", width=100)
        self.contracts_tree.column("start_date", width=100)
        self.contracts_tree.column("end_date", width=100)
        self.contracts_tree.column("status", width=100)
        
        scrollbar = ttk.Scrollbar(contracts_list_frame, orient=tk.VERTICAL, command=self.contracts_tree.yview)
        self.contracts_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.contracts_tree.pack(fill="both", expand=True)
        
        # Button frame
        button_frame = ttk.Frame(contracts_list_frame)
        button_frame.pack(fill="x", pady=5)
        
        refresh_button = ttk.Button(button_frame, text="Refresh", command=self.load_contracts)
        refresh_button.pack(side=tk.LEFT, padx=5)
        
        view_button = ttk.Button(button_frame, text="View Details", command=self.view_contract_details)
        view_button.pack(side=tk.LEFT, padx=5)
        
        if self.current_user["role"] == "client":
            complete_button = ttk.Button(button_frame, text="Mark Complete", command=self.complete_contract)
            complete_button.pack(side=tk.LEFT, padx=5)
        
        review_button = ttk.Button(button_frame, text="Leave Review", command=self.leave_review)
        review_button.pack(side=tk.LEFT, padx=5)
        
        # Load contracts
        self.load_contracts()
    
    def connect_to_database(self):
        try:
            # Try to load config if it exists
            config = configparser.ConfigParser()
            
            if os.path.exists('db_config.ini'):
                config.read('db_config.ini')
                host = config['Database']['host']
                database = config['Database']['database']
                user = config['Database']['user']
                password = config['Database']['password']
                port = config['Database'].get('port', '5432')
            else:
                # Show connection dialog
                self.show_db_connection_dialog()
                return
                
            # Connect to database
            self.connection = psycopg2.connect(
                host=host,
                database=database,
                user=user,
                password=password,
                port=port
            )
            self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
            
            messagebox.showinfo("Connection", "Successfully connected to the database!")
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Connection Error", f"Failed to connect to database: {error}")
            self.show_db_connection_dialog()
    
    def show_db_connection_dialog(self):
        # Create a new window for DB connection
        db_window = tk.Toplevel(self.root)
        db_window.title("Database Connection")
        db_window.geometry("300x250")
        db_window.transient(self.root)
        db_window.grab_set()
        
        ttk.Label(db_window, text="Host:").grid(row=0, column=0, pady=5, padx=5, sticky="w")
        host_entry = ttk.Entry(db_window, width=25)
        host_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
        host_entry.insert(0, "localhost")
        
        ttk.Label(db_window, text="Database:").grid(row=1, column=0, pady=5, padx=5, sticky="w")
        db_entry = ttk.Entry(db_window, width=25)
        db_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(db_window, text="User:").grid(row=2, column=0, pady=5, padx=5, sticky="w")
        user_entry = ttk.Entry(db_window, width=25)
        user_entry.grid(row=2, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(db_window, text="Password:").grid(row=3, column=0, pady=5, padx=5, sticky="w")
        pass_entry = ttk.Entry(db_window, width=25, show="*")
        pass_entry.grid(row=3, column=1, pady=5, padx=5, sticky="w")
        
        ttk.Label(db_window, text="Port:").grid(row=4, column=0, pady=5, padx=5, sticky="w")
        port_entry = ttk.Entry(db_window, width=25)
        port_entry.grid(row=4, column=1, pady=5, padx=5, sticky="w")
        port_entry.insert(0, "5432")
        
        def save_connection():
            config = configparser.ConfigParser()
            config['Database'] = {
                'host': host_entry.get(),
                'database': db_entry.get(),
                'user': user_entry.get(),
                'password': pass_entry.get(),
                'port': port_entry.get()
            }
            
            with open('db_config.ini', 'w') as configfile:
                config.write(configfile)
            
            db_window.destroy()
            self.connect_to_database()
        
        connect_button = ttk.Button(db_window, text="Connect", command=save_connection)
        connect_button.grid(row=5, column=0, columnspan=2, pady=15)
    
    def login(self):
        email = self.login_email.get()
        password = self.login_password.get()
        
        if not email or not password:
            messagebox.showerror("Error", "Please enter both email and password.")
            return
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            self.cursor.execute("""
                SELECT * FROM users WHERE email = %s
            """, (email,))
            
            user = self.cursor.fetchone()
            
            if user and user["password_hash"] == password_hash:
                self.current_user = dict(user)
                messagebox.showinfo("Login", f"Welcome, {user['first_name']}!")
                
                # Setup other tabs
                self.setup_projects_tab()
                self.setup_profile_tab()
                self.setup_messages_tab()
                self.setup_contracts_tab()
                
                # Enable all tabs
                self.notebook.tab(1, state="normal")
                self.notebook.tab(2, state="normal")
                self.notebook.tab(3, state="normal")
                self.notebook.tab(4, state="normal")
                
                # Switch to projects tab
                self.notebook.select(1)
            else:
                messagebox.showerror("Login Failed", "Invalid email or password.")
                
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to login: {error}")
    
    def register(self):
        email = self.reg_email.get()
        password = self.reg_password.get()
        first_name = self.reg_first_name.get()
        last_name = self.reg_last_name.get()
        role = self.reg_role.get()
        
        if not email or not password or not first_name or not last_name or not role:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        
        # Validate email
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        
        # Hash password
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            # Check if email already exists
            self.cursor.execute("""
                SELECT id FROM users WHERE email = %s
            """, (email,))
            
            if self.cursor.fetchone():
                messagebox.showerror("Registration Failed", "Email already exists.")
                return
            
            # Insert new user
            self.cursor.execute("""
                INSERT INTO users (email, password_hash, role, first_name, last_name)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (email, password_hash, role, first_name, last_name))
            
            new_user_id = self.cursor.fetchone()[0]
            
            # Create user profile
            self.cursor.execute("""
                INSERT INTO user_profiles (user_id)
                VALUES (%s)
            """, (new_user_id,))
            
            self.connection.commit()
            messagebox.showinfo("Registration", "Successfully registered! You can now login.")
            
            # Clear registration fields
            self.reg_email.delete(0, tk.END)
            self.reg_password.delete(0, tk.END)
            self.reg_first_name.delete(0, tk.END)
            self.reg_last_name.delete(0, tk.END)
            
        except (Exception, psycopg2.Error) as error:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to register: {error}")
    
    def create_project(self):
        title = self.project_title.get()
        description = self.project_desc.get("1.0", tk.END).strip()
        budget_min = self.project_budget_min.get()
        budget_max = self.project_budget_max.get()
        skills_required = self.project_skills.get()
        
        if not title or not description:
            messagebox.showerror("Error", "Please provide at least a title and description.")
            return
        
        try:
            # Validate budget
            if budget_min and budget_max:
                budget_min = float(budget_min)
                budget_max = float(budget_max)
                
                if budget_min > budget_max:
                    messagebox.showerror("Error", "Minimum budget cannot be greater than maximum budget.")
                    return
            elif budget_min:
                budget_min = float(budget_min)
                budget_max = None
            elif budget_max:
                budget_max = float(budget_max)
                budget_min = None
            else:
                budget_min = None
                budget_max = None
                
            # Insert project
            self.cursor.execute("""
                INSERT INTO projects (client_id, title, description, budget_min, budget_max, skills_required)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (self.current_user["id"], title, description, budget_min, budget_max, skills_required))
            
            self.connection.commit()
            messagebox.showinfo("Success", "Project created successfully!")
            
            # Clear fields
            self.project_title.delete(0, tk.END)
            self.project_desc.delete("1.0", tk.END)
            self.project_budget_min.delete(0, tk.END)
            self.project_budget_max.delete(0, tk.END)
            self.project_skills.delete(0, tk.END)
            
            # Reload projects
            self.load_projects()
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid budget values.")
        except (Exception, psycopg2.Error) as error:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to create project: {error}")
    
    def load_projects(self):
        # Clear current items
        for item in self.projects_tree.get_children():
            self.projects_tree.delete(item)
            
        try:
            # Different queries based on user role
            if self.current_user["role"] == "client":
                self.cursor.execute("""
                            SELECT p.id, p.title, CONCAT(u.first_name, ' ', u.last_name) as client_name,
                            CASE 
                                WHEN p.budget_min IS NOT NULL AND p.budget_max IS NOT NULL THEN CONCAT('$', p.budget_min, ' - $', p.budget_max)
                                WHEN p.budget_min IS NOT NULL THEN CONCAT('$', p.budget_min, '+')
                                WHEN p.budget_max IS NOT NULL THEN CONCAT('Up to $', p.budget_max)
                                ELSE 'Not specified'
                            END as budget,
                            p.status, p.created_at
                            FROM projects p
                            JOIN users u ON p.client_id = u.id
                            WHERE p.client_id = %s
                            ORDER BY p.created_at DESC
                          """, (self.current_user["id"],))
            else:  # freelancer
                self.cursor.execute("""
                    SELECT p.id, p.title, CONCAT(u.first_name, ' ', u.last_name) as client_name,
                    CASE 
                        WHEN p.budget_min IS NOT NULL AND p.budget_max IS NOT NULL THEN CONCAT('$', p.budget_min, ' - $', p.budget_max)
                        WHEN p.budget_min IS NOT NULL THEN CONCAT('$', p.budget_min, '+')
                        WHEN p.budget_max IS NOT NULL THEN CONCAT('Up to $', p.budget_max)
                        ELSE 'Not specified'
                    END as budget,
                    p.status, p.created_at
                    FROM projects p
                    JOIN users u ON p.client_id = u.id
                    WHERE p.status = 'open'
                    ORDER BY p.created_at DESC
                """)
                
            projects = self.cursor.fetchall()
            
            for project in projects:
                formatted_date = project["created_at"].strftime("%Y-%m-%d %H:%M")
                self.projects_tree.insert("", "end", values=(
                    project["id"], 
                    project["title"], 
                    project["client_name"], 
                    project["budget"], 
                    project["status"], 
                    formatted_date
                ))
                
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load projects: {error}")
    
    def view_project_details(self):
        selected_item = self.projects_tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Info", "Please select a project to view.")
            return
            
        project_id = self.projects_tree.item(selected_item[0])["values"][0]
        
        try:
            # Get project details
            self.cursor.execute("""
                SELECT p.*, CONCAT(u.first_name, ' ', u.last_name) as client_name
                FROM projects p
                JOIN users u ON p.client_id = u.id
                WHERE p.id = %s
            """, (project_id,))
            
            project = self.cursor.fetchone()
            
            if not project:
                messagebox.showerror("Error", "Project not found.")
                return
                
            # Get bids if client
            bids_info = ""
            if self.current_user["role"] == "client" and self.current_user["id"] == project["client_id"]:
                self.cursor.execute("""
                    SELECT b.*, CONCAT(u.first_name, ' ', u.last_name) as freelancer_name
                    FROM bids b
                    JOIN users u ON b.freelancer_id = u.id
                    WHERE b.project_id = %s
                    ORDER BY b.created_at
                """, (project_id,))
                
                bids = self.cursor.fetchall()
                
                if bids:
                    bids_info = "\n\nBids:\n"
                    for bid in bids:
                        bids_info += f"- {bid['freelancer_name']}: ${bid['amount']} ({bid['duration_days']} days) - {bid['status'].upper()}\n"
                else:
                    bids_info = "\n\nNo bids yet."
            
            # Create details window
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Project: {project['title']}")
            details_window.geometry("600x500")
            details_window.transient(self.root)
            
            # Project details
            ttk.Label(details_window, text="Project Details", font=("Arial", 16, "bold")).pack(pady=10)
            
            details_frame = ttk.Frame(details_window)
            details_frame.pack(fill="both", expand=True, padx=20, pady=10)
            
            details_text = f"""Title: {project['title']}
Client: {project['client_name']}
Status: {project['status'].upper()}
Created: {project['created_at'].strftime("%Y-%m-%d %H:%M")}

Budget: {f"${project['budget_min']} - ${project['budget_max']}" if project['budget_min'] and project['budget_max'] else
         f"${project['budget_min']}+" if project['budget_min'] else
         f"Up to ${project['budget_max']}" if project['budget_max'] else "Not specified"}

Skills Required: {project['skills_required'] if project['skills_required'] else "Not specified"}

Description:
{project['description']}
{bids_info}
"""
            
            text_widget = tk.Text(details_frame, wrap=tk.WORD)
            text_widget.pack(fill="both", expand=True)
            text_widget.insert(tk.END, details_text)
            text_widget.config(state=tk.DISABLED)
            
            ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load project details: {error}")
    
    def place_bid(self):
        selected_item = self.projects_tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Info", "Please select a project to bid on.")
            return
            
        project_id = self.projects_tree.item(selected_item[0])["values"][0]
        
        # Check if already bid
        try:
            self.cursor.execute("""
                SELECT id FROM bids 
                WHERE project_id = %s AND freelancer_id = %s
            """, (project_id, self.current_user["id"]))
            
            if self.cursor.fetchone():
                messagebox.showinfo("Info", "You have already placed a bid on this project.")
                return
                
            # Create bid dialog
            bid_window = tk.Toplevel(self.root)
            bid_window.title("Place Bid")
            bid_window.geometry("400x350")
            bid_window.transient(self.root)
            bid_window.grab_set()
            
            ttk.Label(bid_window, text="Amount ($):").grid(row=0, column=0, pady=5, padx=10, sticky="w")
            amount_entry = ttk.Entry(bid_window, width=15)
            amount_entry.grid(row=0, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(bid_window, text="Duration (days):").grid(row=1, column=0, pady=5, padx=10, sticky="w")
            duration_entry = ttk.Entry(bid_window, width=15)
            duration_entry.grid(row=1, column=1, pady=5, padx=5, sticky="w")
            
            ttk.Label(bid_window, text="Proposal:").grid(row=2, column=0, pady=5, padx=10, sticky="w")
            proposal_text = tk.Text(bid_window, width=40, height=10)
            proposal_text.grid(row=3, column=0, columnspan=2, pady=5, padx=10, sticky="we")
            
            def submit_bid():
                try:
                    amount = float(amount_entry.get())
                    duration = int(duration_entry.get())
                    proposal = proposal_text.get("1.0", tk.END).strip()
                    
                    if amount <= 0 or duration <= 0 or not proposal:
                        messagebox.showerror("Error", "Please fill in all fields with valid values.")
                        return
                        
                    self.cursor.execute("""
                        INSERT INTO bids (project_id, freelancer_id, amount, duration_days, proposal)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (project_id, self.current_user["id"], amount, duration, proposal))
                    
                    self.connection.commit()
                    messagebox.showinfo("Success", "Bid placed successfully!")
                    bid_window.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter valid numeric values.")
                except (Exception, psycopg2.Error) as error:
                    self.connection.rollback()
                    messagebox.showerror("Database Error", f"Failed to place bid: {error}")
            
            ttk.Button(bid_window, text="Submit Bid", command=submit_bid).grid(row=4, column=0, columnspan=2, pady=15)
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to check bid status: {error}")
    
    def manage_project(self):
        selected_item = self.projects_tree.selection()
        
        if not selected_item:
            messagebox.showinfo("Info", "Please select a project to manage.")
            return
            
        project_id = self.projects_tree.item(selected_item[0])["values"][0]
        
        try:
            # Check if user owns this project
            self.cursor.execute("""
                SELECT id FROM projects 
                WHERE id = %s AND client_id = %s
            """, (project_id, self.current_user["id"]))
            
            if not self.cursor.fetchone():
                messagebox.showerror("Error", "You can only manage your own projects.")
                return
                
            # Get bids for this project
            self.cursor.execute("""
                SELECT b.*, CONCAT(u.first_name, ' ', u.last_name) as freelancer_name,
                       up.avg_rating
                FROM bids b
                JOIN users u ON b.freelancer_id = u.id
                LEFT JOIN user_profiles up ON u.id = up.user_id
                WHERE b.project_id = %s
                ORDER BY b.created_at
            """, (project_id,))
            
            bids = self.cursor.fetchall()
            
            if not bids:
                messagebox.showinfo("Info", "No bids received for this project yet.")
                return
            
            # Create management window
            manage_window = tk.Toplevel(self.root)
            manage_window.title("Manage Project Bids")
            manage_window.geometry("800x500")
            manage_window.transient(self.root)
            
            # Create treeview for bids
            columns = ("id", "freelancer", "amount", "duration", "status", "rating", "created_at")
            bids_tree = ttk.Treeview(manage_window, columns=columns, show="headings")
            
            bids_tree.heading("id", text="ID")
            bids_tree.heading("freelancer", text="Freelancer")
            bids_tree.heading("amount", text="Amount")
            bids_tree.heading("duration", text="Duration (days)")
            bids_tree.heading("status", text="Status")
            bids_tree.heading("rating", text="Rating")
            bids_tree.heading("created_at", text="Created At")
            
            bids_tree.column("id", width=50)
            bids_tree.column("freelancer", width=150)
            bids_tree.column("amount", width=80)
            bids_tree.column("duration", width=100)
            bids_tree.column("status", width=80)
            bids_tree.column("rating", width=80)
            bids_tree.column("created_at", width=150)
            
            scrollbar = ttk.Scrollbar(manage_window, orient=tk.VERTICAL, command=bids_tree.yview)
            bids_tree.configure(yscroll=scrollbar.set)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            bids_tree.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Populate bids
            for bid in bids:
                formatted_date = bid["created_at"].strftime("%Y-%m-%d %H:%M")
                rating = f"{bid['avg_rating']:.1f}" if bid["avg_rating"] else "N/A"
                
                bids_tree.insert("", "end", values=(
                    bid["id"],
                    bid["freelancer_name"],
                    f"${bid['amount']}",
                    bid["duration_days"],
                    bid["status"].upper(),
                    rating,
                    formatted_date
                ))
            
            # Button frame
            button_frame = ttk.Frame(manage_window)
            button_frame.pack(fill="x", padx=10, pady=10)
            
            def view_proposal():
                selected = bids_tree.selection()
                if not selected:
                    messagebox.showinfo("Info", "Please select a bid to view.")
                    return
                    
                bid_id = bids_tree.item(selected[0])["values"][0]
                
                # Find the bid in our list
                bid_data = next((b for b in bids if b["id"] == bid_id), None)
                
                if bid_data:
                    proposal_window = tk.Toplevel(manage_window)
                    proposal_window.title("Bid Proposal")
                    proposal_window.geometry("500x300")
                    proposal_window.transient(manage_window)
                    
                    ttk.Label(proposal_window, text=f"Proposal from {bid_data['freelancer_name']}", 
                             font=("Arial", 12, "bold")).pack(pady=10)
                    
                    proposal_text = tk.Text(proposal_window, wrap=tk.WORD)
                    proposal_text.pack(fill="both", expand=True, padx=10)
                    proposal_text.insert(tk.END, bid_data["proposal"])
                    proposal_text.config(state=tk.DISABLED)
                    
                    ttk.Button(proposal_window, text="Close", command=proposal_window.destroy).pack(pady=10)
            
            def accept_bid():
                selected = bids_tree.selection()
                if not selected:
                    messagebox.showinfo("Info", "Please select a bid to accept.")
                    return
                    
                bid_id = bids_tree.item(selected[0])["values"][0]
                
                if messagebox.askyesno("Confirm", "Are you sure you want to accept this bid? This will create a contract."):
                    try:
                        # Get bid info
                        self.cursor.execute("""
                            SELECT * FROM bids WHERE id = %s
                        """, (bid_id,))
                        
                        bid_data = self.cursor.fetchone()
                        
                        # Get project info
                        self.cursor.execute("""
                            SELECT title FROM projects WHERE id = %s
                        """, (project_id,))
                        
                        project_data = self.cursor.fetchone()
                        
                        # Calculate end date (start date + duration)
                        start_date = datetime.now().date()
                        end_date = start_date + timedelta(days=bid_data["duration_days"])
                        
                        # Start transaction
                        self.cursor.execute("BEGIN")
                        
                        # Update bid status
                        self.cursor.execute("""
                            UPDATE bids SET status = 'accepted' WHERE id = %s
                        """, (bid_id,))
                        
                        # Reject other bids
                        self.cursor.execute("""
                            UPDATE bids SET status = 'rejected' 
                            WHERE project_id = %s AND id != %s
                        """, (project_id, bid_id))
                        
                        # Update project status
                        self.cursor.execute("""
                            UPDATE projects SET status = 'in_progress' WHERE id = %s
                        """, (project_id,))
                        
                        # Create contract
                        self.cursor.execute("""
                            INSERT INTO contracts (
                                project_id, bid_id, client_id, freelancer_id, 
                                title, amount, start_date, end_date
                            )
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            project_id, bid_id, self.current_user["id"], 
                            bid_data["freelancer_id"], project_data["title"],
                            bid_data["amount"], start_date, end_date
                        ))
                        
                        self.connection.commit()
                        messagebox.showinfo("Success", "Bid accepted and contract created!")
                        manage_window.destroy()
                        
                        # Refresh projects list
                        self.load_projects()
                        
                    except (Exception, psycopg2.Error) as error:
                        self.connection.rollback()
                        messagebox.showerror("Database Error", f"Failed to accept bid: {error}")
            
            view_button = ttk.Button(button_frame, text="View Proposal", command=view_proposal)
            view_button.pack(side=tk.LEFT, padx=5)
            
            accept_button = ttk.Button(button_frame, text="Accept Bid", command=accept_bid)
            accept_button.pack(side=tk.LEFT, padx=5)
            
            close_button = ttk.Button(button_frame, text="Close", command=manage_window.destroy)
            close_button.pack(side=tk.RIGHT, padx=5)
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to manage project: {error}")
    
    def save_profile(self):
        # Get basic profile info
        first_name = self.profile_first_name.get()
        last_name = self.profile_last_name.get()
        bio = self.profile_bio.get("1.0", tk.END).strip()
        
        if not first_name or not last_name:
            messagebox.showerror("Error", "First name and last name are required.")
            return
            
        try:
            # Update user table
            self.cursor.execute("""
                UPDATE users 
                SET first_name = %s, last_name = %s, bio = %s
                WHERE id = %s
            """, (first_name, last_name, bio, self.current_user["id"]))
            
            # Update user profile based on role
            if self.current_user["role"] == "freelancer":
                headline = self.profile_headline.get()
                hourly_rate = self.profile_hourly_rate.get()
                skills = self.profile_skills.get()
                
                # Validate hourly rate if provided
                if hourly_rate:
                    try:
                        hourly_rate = float(hourly_rate)
                    except ValueError:
                        messagebox.showerror("Error", "Hourly rate must be a number.")
                        return
                else:
                    hourly_rate = None
                
                self.cursor.execute("""
                    UPDATE user_profiles
                    SET headline = %s, hourly_rate = %s, skills = %s
                    WHERE user_id = %s
                """, (headline, hourly_rate, skills, self.current_user["id"]))
                
            elif self.current_user["role"] == "client":
                company_name = self.profile_company.get()
                
                self.cursor.execute("""
                    UPDATE user_profiles
                    SET company_name = %s
                    WHERE user_id = %s
                """, (company_name, self.current_user["id"]))
            
            self.connection.commit()
            
            # Update current user info
            self.current_user["first_name"] = first_name
            self.current_user["last_name"] = last_name
            self.current_user["bio"] = bio
            
            messagebox.showinfo("Success", "Profile updated successfully!")
            
        except (Exception, psycopg2.Error) as error:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to update profile: {error}")
    
    def new_message(self):
        # Show dialog to select user
        select_window = None
        try:
            # Get users except current user
            self.cursor.execute("""
                SELECT id, first_name, last_name, role FROM users
                WHERE id != %s
                ORDER BY first_name, last_name
            """, (self.current_user["id"],))
            
            users = self.cursor.fetchall()
            
            if not users:
                messagebox.showinfo("Info", "No users found to message.")
                return
                
            # Create user selection dialog
            select_window = tk.Toplevel(self.root)
            select_window.title("Select User")
            select_window.geometry("400x300")
            select_window.transient(self.root)
            select_window.grab_set()
            
            ttk.Label(select_window, text="Select a user to message:").pack(pady=10)
            
            user_listbox = tk.Listbox(select_window, width=40, height=10)
            user_listbox.pack(fill="both", expand=True, padx=10, pady=5)
            
            user_map = {}  # Map listbox index to user ID
            for idx, user in enumerate(users):
                display_text = f"{user['first_name']} {user['last_name']} ({user['role']})"
                user_listbox.insert(tk.END, display_text)
                user_map[idx] = user['id']
            
            def select_user():
                selected = user_listbox.curselection()
                if not selected:
                    messagebox.showinfo("Info", "Please select a user.")
                    return
                
                selected_idx = selected[0]
                self.current_message_recipient = user_map[selected_idx]
                select_window.destroy()
                
                # Refresh conversations and messages
                self.load_conversations()
                self.load_conversation_messages()

                # Switch to messages tab
                self.notebook.select(self.messages_frame)

            select_button = ttk.Button(select_window, text="Select", command=select_user)
            select_button.pack(pady=10)
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load users: {error}")
            if select_window:
                select_window.destroy()

    def load_conversations(self):
        # Clear current items
        for item in self.conversations_tree.get_children():
            self.conversations_tree.delete(item)
            
        try:
            # Get unique conversations
            self.cursor.execute("""
                SELECT DISTINCT 
                    CASE
                        WHEN sender_id = %s THEN receiver_id
                        ELSE sender_id
                    END as user_id,
                    COUNT(*) FILTER (WHERE receiver_id = %s AND is_read = FALSE) as unread_count
                FROM messages
                WHERE sender_id = %s OR receiver_id = %s
                GROUP BY user_id
                ORDER BY unread_count DESC
            """, (self.current_user["id"], self.current_user["id"], self.current_user["id"], self.current_user["id"]))
            
            conversations = self.cursor.fetchall()
            
            for conversation in conversations:
                # Get user name
                self.cursor.execute("""
                    SELECT first_name, last_name FROM users WHERE id = %s
                """, (conversation["user_id"],))
                
                user = self.cursor.fetchone()
                user_name = f"{user['first_name']} {user['last_name']}"
                
                unread = conversation["unread_count"] if conversation["unread_count"] else 0
                
                self.conversations_tree.insert("", "end", values=(
                    conversation["user_id"],
                    user_name,
                    unread
                ))
                
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load conversations: {error}")

    def load_conversation_messages(self, event=None):
        selected_item = self.conversations_tree.selection()
        
        if not selected_item:
            return
            
        user_id = self.conversations_tree.item(selected_item[0])["values"][0]
        
        try:
            # Mark messages as read
            self.cursor.execute("""
                UPDATE messages
                SET is_read = TRUE
                WHERE sender_id = %s AND receiver_id = %s
            """, (user_id, self.current_user["id"]))
            
            self.connection.commit()
            
            # Refresh unread count
            self.load_conversations()
            
            # Get all messages between current user and selected user
            self.cursor.execute("""
                SELECT m.*, 
                       CONCAT(s.first_name, ' ', s.last_name) as sender_name,
                       CONCAT(r.first_name, ' ', r.last_name) as receiver_name
                FROM messages m
                JOIN users s ON m.sender_id = s.id
                JOIN users r ON m.receiver_id = r.id
                WHERE (m.sender_id = %s AND m.receiver_id = %s) OR
                       (m.sender_id = %s AND m.receiver_id = %s)
                ORDER BY m.created_at
            """, (self.current_user["id"], user_id, user_id, self.current_user["id"]))
            
            messages = self.cursor.fetchall()
            
            # Clear and display messages
            self.messages_text.config(state=tk.NORMAL)
            self.messages_text.delete("1.0", tk.END)
            
            for message in messages:
                timestamp = message["created_at"].strftime("%Y-%m-%d %H:%M")
                
                if message["sender_id"] == self.current_user["id"]:
                    sender_text = "You"
                    self.messages_text.insert(tk.END, f"{sender_text} ({timestamp}):\n", "right")
                    self.messages_text.insert(tk.END, f"{message['message']}\n\n", "right_text")
                else:
                    sender_text = message["sender_name"]
                    self.messages_text.insert(tk.END, f"{sender_text} ({timestamp}):\n", "left")
                    self.messages_text.insert(tk.END, f"{message['message']}\n\n", "left_text")
            
            self.messages_text.config(state=tk.DISABLED)
            
            # Store current recipient for send_message function
            self.current_message_recipient = user_id
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load messages: {error}")

    def send_message(self):
        if not hasattr(self, "current_message_recipient"):
            messagebox.showinfo("Info", "Please select a conversation first.")
            return
            
        message_text = self.message_entry.get("1.0", tk.END).strip()
        
        if not message_text:
            return
            
        try:
            # Insert message
            self.cursor.execute("""
                INSERT INTO messages (sender_id, receiver_id, message)
                VALUES (%s, %s, %s)
            """, (self.current_user["id"], self.current_message_recipient, message_text))
            
            self.connection.commit()
            
            # Clear message entry
            self.message_entry.delete("1.0", tk.END)
            
            # Reload conversation
            self.load_conversation_messages()
            
        except (Exception, psycopg2.Error) as error:
            self.connection.rollback()
            messagebox.showerror("Database Error", f"Failed to send message: {error}")

    def load_contracts(self):
        # Clear current items
        for item in self.contracts_tree.get_children():
            self.contracts_tree.delete(item)
            
        try:
            # Different query based on user role
            if self.current_user["role"] == "client":
                self.cursor.execute("""
                    SELECT c.*, u.first_name || ' ' || u.last_name as freelancer_name
                    FROM contracts c
                    JOIN users u ON c.freelancer_id = u.id
                    WHERE c.client_id = %s
                    ORDER BY c.start_date DESC
                """, (self.current_user["id"],))
            else:
                self.cursor.execute("""
                    SELECT c.*, u.first_name || ' ' || u.last_name as client_name
                    FROM contracts c
                    JOIN users u ON c.client_id = u.id
                    WHERE c.freelancer_id = %s
                    ORDER BY c.start_date DESC
                """, (self.current_user["id"],))
                
            contracts = self.cursor.fetchall()
            
            for contract in contracts:
                with_user = (contract["freelancer_name"] if self.current_user["role"] == "client"
                              else contract["client_name"])
                status = contract["status"].replace("_", " ").title()
                start_date = contract["start_date"].strftime("%Y-%m-%d")
                end_date = contract["end_date"].strftime("%Y-%m-%d") if contract["end_date"] else "N/A"
                
                self.contracts_tree.insert("", "end", values=(
                    contract["id"],
                    contract["title"],
                    with_user,
                    f"${contract['amount']}",
                    start_date,
                    end_date,
                    status
                ))
                
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load contracts: {error}")

    def view_contract_details(self):
        selected_item = self.contracts_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a contract.")
            return
            
        contract_id = self.contracts_tree.item(selected_item[0])["values"][0]
        
        try:
            self.cursor.execute("""
                SELECT c.*, 
                       cl.first_name || ' ' || cl.last_name as client_name,
                       fl.first_name || ' ' || fl.last_name as freelancer_name
                FROM contracts c
                JOIN users cl ON c.client_id = cl.id
                JOIN users fl ON c.freelancer_id = fl.id
                WHERE c.id = %s
            """, (contract_id,))
            
            contract = self.cursor.fetchone()
            
            details_window = tk.Toplevel(self.root)
            details_window.title(f"Contract Details - {contract['title']}")
            details_window.geometry("600x400")
            
            text_widget = tk.Text(details_window, wrap=tk.WORD)
            text_widget.pack(fill="both", expand=True, padx=10, pady=10)
            
            details = f"""Contract ID: {contract['id']}
                          Title: {contract['title']}
                          Client: {contract['client_name']}
                          Freelancer: {contract['freelancer_name']}
                          Amount: ${contract['amount']}
                          Start Date: {contract['start_date'].strftime("%Y-%m-%d")}
                          End Date: {contract['end_date'].strftime("%Y-%m-%d") if contract['end_date'] else 'Ongoing'}
                          Status: {contract['status'].replace('_', ' ').title()}
                          """
            text_widget.insert(tk.END, details)
            text_widget.config(state=tk.DISABLED)
            
            ttk.Button(details_window, text="Close", command=details_window.destroy).pack(pady=10)
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load contract: {error}")

    def complete_contract(self):
        selected_item = self.contracts_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a contract.")
            return
            
        contract_id = self.contracts_tree.item(selected_item[0])["values"][0]
        
        if messagebox.askyesno("Confirm", "Mark this contract as completed?"):
            try:
                self.cursor.execute("""
                    UPDATE contracts 
                    SET status = 'completed', end_date = CURRENT_DATE
                    WHERE id = %s AND client_id = %s
                """, (contract_id, self.current_user["id"]))
                
                self.connection.commit()
                messagebox.showinfo("Success", "Contract marked as completed.")
                self.load_contracts()
                
            except (Exception, psycopg2.Error) as error:
                self.connection.rollback()
                messagebox.showerror("Database Error", f"Failed to update contract: {error}")

    def leave_review(self):
        selected_item = self.contracts_tree.selection()
        if not selected_item:
            messagebox.showinfo("Info", "Please select a contract.")
            return
            
        contract_id = self.contracts_tree.item(selected_item[0])["values"][0]
        
        try:
            # Check if review already exists
            self.cursor.execute("""
                SELECT id FROM reviews 
                WHERE contract_id = %s AND reviewer_id = %s
            """, (contract_id, self.current_user["id"]))
            
            if self.cursor.fetchone():
                messagebox.showinfo("Info", "You've already reviewed this contract.")
                return
                
            # Get contract details
            self.cursor.execute("""
                SELECT client_id, freelancer_id 
                FROM contracts 
                WHERE id = %s
            """, (contract_id,))
            
            contract = self.cursor.fetchone()
            reviewee_id = (contract["freelancer_id"] if self.current_user["role"] == "client"
                           else contract["client_id"])
            
            # Review dialog
            review_window = tk.Toplevel(self.root)
            review_window.title("Leave Review")
            review_window.geometry("400x300")
            
            ttk.Label(review_window, text="Rating (1-5):").pack(pady=5)
            rating_entry = ttk.Entry(review_window)
            rating_entry.pack(pady=5)
            
            ttk.Label(review_window, text="Comments:").pack(pady=5)
            comment_text = tk.Text(review_window, height=8)
            comment_text.pack(pady=5, fill="x")
            
            def submit_review():
                try:
                    rating = int(rating_entry.get())
                    if rating < 1 or rating > 5:
                        raise ValueError
                        
                    comment = comment_text.get("1.0", tk.END).strip()
                    
                    self.cursor.execute("""
                        INSERT INTO reviews (
                            contract_id, reviewer_id, reviewee_id, 
                            rating, comment
                        )
                        VALUES (%s, %s, %s, %s, %s)
                    """, (contract_id, self.current_user["id"], reviewee_id, rating, comment))
                    
                    self.connection.commit()
                    messagebox.showinfo("Success", "Review submitted successfully!")
                    review_window.destroy()
                    
                except ValueError:
                    messagebox.showerror("Error", "Please enter a valid rating (1-5).")
                except (Exception, psycopg2.Error) as error:
                    self.connection.rollback()
                    messagebox.showerror("Database Error", f"Failed to submit review: {error}")
            
            ttk.Button(review_window, text="Submit", command=submit_review).pack(pady=10)
            
        except (Exception, psycopg2.Error) as error:
            messagebox.showerror("Database Error", f"Failed to load contract: {error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FreelancePlatformApp(root)
    root.mainloop()
