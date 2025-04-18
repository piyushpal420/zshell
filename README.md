# ZSHELL Terminal

> A hybrid GUI shell project combining the power of C and Python — part of the Software Engineering Project-Based Learning course.

###  Developed by:
[**Piyush Pal**](https://github.com/piyushpal420), **Mehdi Zaidi**, **Kirri Tharun**, and **Tushar Dwivedi**

---

## ✨ Features

- 🎨 **GUI in Python (Tkinter)**  
  Customize your shell experience with adjustable appearance settings.

- ⚙️ **Shell Logic in C**  
  Efficiently handles Unix-based system calls.

- 📖 **GNU ReadLine Integration**  
  Provides command-line editing, history, and enhanced input handling.

---




## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/piyushpal420/zshell.git
```
### 2. Then simply run the **frontend.py** file to start the GUI shell.

```bash
python3 frontend.py
```
## Shell C Compilation Process
> #### NOTE: This code will run only on UNIX/LINUX systems so either install WSL on your windows or use a VM with ubuntu.
### 1. Install GNU's readLine library using:-

```bash
sudo apt-get install libreadline-dev
```

### 2. After its finished installing, your system is now ready to run readLine library function.

### 3. For running test.c, you can just execute the a.out.

### 4. And if you want to make changes and compile test.c then:-
```bash
gcc test.c -lreadline -lcurses
```
                                                                
> This line adds linkage with the GNU Readline library. I have made use of readline() and add_history() functions, which are part of the readline library, which cannot be used without linking it during compilation.
---

## 🛠️ Technologies Used

| Component       | Language         |
|----------------|------------------|
| GUI            | Python (Tkinter) |
| Shell Logic    | C                |
| Command Parser | GNU ReadLine     |

---

## 📌 Notes

- Designed for **Unix-based systems** (Linux/macOS).
- Ensure `readline` and `tkinter` are installed on your system.

---

## 📷 Preview

<!-- Add screenshots or demo GIFs here if available -->
![Preview](./asset/screenshot1.png)
![Preview](./asset/screenshot1.png)
---

## 📄 License

MIT License © 2025 ZSHELL Contributors
