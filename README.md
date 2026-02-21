# 16x2_lcd_character_creator
A simple python tool to create 8x5 Characters for 16x2 Displays

Works with Arduino UNO/Nano/Mega (or basically anything that just supports the 16x2 lcd module)

# How to Use

1. Launch the file using ```python3 main.py```
2. Create the Character
3. Copy the Custom Character code you made under the matrix buttons
4. Paste it in Arduino ide
5. Initialize it in the void setup Like this
   ```
   void setup() {
     lcd.begin(16, 2);
     lcd.createChar(0, customChar); 
  
     lcd.setCursor(0, 0);
     lcd.write(byte(0)); 
     lcd.print(" Now Playing");
   }
   ```

# Screenshot

<img width="1123" height="513" alt="Screenshot 2026-02-21 at 12 35 05 PM" src="https://github.com/user-attachments/assets/8c9557c4-0f39-48b8-9554-b1c9d9c69be2" />
