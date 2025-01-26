You are an experienced front-end developer. Follow these instructions strictly:

### **🔹 Project Goal**
- Build a simple **resume beautification tool** that takes raw resume content (from PDF, Word, or TXT) and generates a styled PDF based on a **custom Figma design**.

### **🔹 Core Requirements**
1️⃣ **Input Handling**
   - Users upload a resume in **PDF, DOCX, or TXT format**.
   - Extract plain text content from the file.
   - Store extracted data in a structured format (e.g., JSON object).

2️⃣ **UI & Layout Customization**
   - Implement an **HTML + Tailwind CSS** layout that follows a **provided Figma design**.
   - Allow users to edit **text content** directly on the webpage.
   - Provide **basic color theme switching** (light/dark modes, or predefined color palettes).
   - Enable **layout modifications** (e.g., single-column vs. multi-column).

3️⃣ **PDF Generation**
   - Convert the styled **HTML + Tailwind CSS** resume into a **high-quality PDF**.
   - Use `WeasyPrint` or `wkhtmltopdf` to ensure proper rendering.
   - Maintain layout consistency across different devices and print settings.

4️⃣ **Localization Support**
   - Detect if the input content is **English or Chinese**, and apply the corresponding language layout and font.

### **🔹 Additional Constraints**
🚫 Do NOT use React or other JavaScript frameworks unless explicitly requested.
🚫 Do NOT store or process user data on a backend server; everything runs locally in the browser.
🚫 Keep dependencies minimal and lightweight.

---

### **🔹 Now, generate the necessary HTML + Tailwind CSS code for a resume template based on the Figma design.**
