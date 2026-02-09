import random
import time
import tkinter as tk
from tkinter import ttk, messagebox

# ---------- Statistics ----------
stats = {
    "games": 0,
    "wins": 0,
    "losses": 0,
    "total_bet": 0,
    "profit": 0
}

def update_stats(bet, result):
    stats["games"] += 1
    stats["total_bet"] += bet
    stats["profit"] += result

    if result > 0:
        stats["wins"] += 1
    else:
        stats["losses"] += 1

def show_stats():
    if stats["games"] == 0:
        return "📊 Нет данных"
    
    winrate = (stats["wins"] / stats["games"]) * 100
    return f"""📊 СТАТИСТИКА
-----------------------
🎮 Игр сыграно: {stats["games"]}
✅ Побед: {stats["wins"]}
❌ Поражений: {stats["losses"]}
📈 Winrate: {winrate:.2f}%
💸 Всего поставлено: {stats["total_bet"]}
💰 Профит: {stats["profit"]}"""

# ---------- Casino GUI ----------
class CasinoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎰 Mini Casino 🎰")
        self.root.geometry("700x600")
        self.root.configure(bg="#1a1a2e")
        
        # Центрирование окна
        self.center_window()
        
        self.balance = 1000
        self.current_game = None
        self.bet_amount = tk.IntVar(value=100)
        self.game_result = tk.StringVar(value="")
        
        # Список символов слотов с их цветами
        self.symbols = [
            {"emoji": "🍒", "color": "#e74c3c", "name": "Вишня"},      # Красный
            {"emoji": "🍋", "color": "#f1c40f", "name": "Лимон"},      # Желтый
            {"emoji": "🔔", "color": "#f39c12", "name": "Колокол"},    # Оранжевый
            {"emoji": "💎", "color": "#3498db", "name": "Алмаз"},      # Синий
            {"emoji": "⭐", "color": "#f1c40f", "name": "Звезда"},     # Золотой
            {"emoji": "7️⃣", "color": "#e74c3c", "name": "Семерка"}     # Красный
        ]
        
        self.game_play_button = None  # Кнопка "Играть"
        self.slot_labels = []  # Ярлыки для слотов
        self.setup_ui()
        self.update_balance_display()
        
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def get_symbol_color(self, emoji):
        """Возвращает цвет для символа эмодзи"""
        for symbol in self.symbols:
            if symbol["emoji"] == emoji:
                return symbol["color"]
        return "#ffffff"  # Белый по умолчанию
    
    def get_symbol_name(self, emoji):
        """Возвращает название для символа эмодзи"""
        for symbol in self.symbols:
            if symbol["emoji"] == emoji:
                return symbol["name"]
        return emoji
    
    def setup_ui(self):
        # Создаем основной контейнер
        main_container = tk.Frame(self.root, bg="#1a1a2e")
        main_container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Заголовок
        title_frame = tk.Frame(main_container, bg="#16213e", height=70)
        title_frame.pack(fill="x", pady=(0, 10))
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(title_frame, text="🎰 MINI CASINO 🎰", 
                              font=("Arial", 28, "bold"), 
                              fg="#00b4d8", bg="#16213e")
        title_label.pack(expand=True)
        
        # Панель баланса в центре
        balance_frame = tk.Frame(main_container, bg="#0f3460", height=60)
        balance_frame.pack(fill="x", pady=5)
        balance_frame.pack_propagate(False)
        
        self.balance_label = tk.Label(balance_frame, text="", 
                                      font=("Arial", 18, "bold"), 
                                      fg="#ffffff", bg="#0f3460")
        self.balance_label.pack(expand=True)
        
        # Основной контент - две колонки
        content_frame = tk.Frame(main_container, bg="#1a1a2e")
        content_frame.pack(fill="both", expand=True, pady=10)
        
        # Левая колонка - игры
        left_frame = tk.Frame(content_frame, bg="#1a1a2e", width=300)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        # Правая колонка - результаты и управление
        right_frame = tk.Frame(content_frame, bg="#1a1a2e", width=300)
        right_frame.pack(side="right", fill="both", expand=True, padx=(10, 0))
        
        # Стили для кнопок игр
        button_style = {
            "font": ("Arial", 13, "bold"),
            "width": 18,
            "height": 2,
            "relief": "raised",
            "bd": 3
        }
        
        # Кнопки выбора игр
        games_label = tk.Label(left_frame, text="🎮 ВЫБЕРИТЕ ИГРУ", 
                              font=("Arial", 14, "bold"),
                              bg="#1a1a2e", fg="#e94560")
        games_label.pack(pady=(0, 15))
        
        self.coin_button = tk.Button(left_frame, text="🪙 COIN FLIP", 
                                     command=self.setup_coin_flip,
                                     bg="#3498db", fg="white", 
                                     activebackground="#2980b9",
                                     **button_style)
        self.coin_button.pack(pady=8)
        
        self.dice_button = tk.Button(left_frame, text="🎲 DICE", 
                                     command=self.setup_dice,
                                     bg="#9b59b6", fg="white",
                                     activebackground="#8e44ad",
                                     **button_style)
        self.dice_button.pack(pady=8)
        
        self.slots_button = tk.Button(left_frame, text="🎰 SLOTS", 
                                      command=self.setup_slots,
                                      bg="#e74c3c", fg="white",
                                      activebackground="#c0392b",
                                      **button_style)
        self.slots_button.pack(pady=8)
        
        self.stats_button = tk.Button(left_frame, text="📊 СТАТИСТИКА", 
                                      command=self.show_stats_gui,
                                      bg="#f39c12", fg="white",
                                      activebackground="#d35400",
                                      **button_style)
        self.stats_button.pack(pady=8)
        
        # Правая колонка - Ставка
        bet_frame = tk.LabelFrame(right_frame, text=" 💰 СТАВКА ", 
                                 font=("Arial", 12, "bold"),
                                 bg="#16213e", fg="#00b4d8",
                                 relief="ridge", bd=2)
        bet_frame.pack(fill="x", pady=(0, 20))
        
        tk.Label(bet_frame, text="Сумма ставки:", 
                bg="#16213e", fg="#ffffff", 
                font=("Arial", 11)).pack(pady=10)
        
        # Поле для ввода ставки
        bet_entry_frame = tk.Frame(bet_frame, bg="#16213e")
        bet_entry_frame.pack(pady=5)
        
        bet_entry = tk.Entry(bet_entry_frame, textvariable=self.bet_amount, 
                            width=15, font=("Arial", 14, "bold"), 
                            justify="center", bd=3, relief="sunken")
        bet_entry.pack()
        
        # Кнопки быстрой ставки
        quick_bet_frame = tk.Frame(bet_frame, bg="#16213e")
        quick_bet_frame.pack(pady=10)
        
        quick_bets = [50, 100, 200, 500]
        for bet in quick_bets:
            btn = tk.Button(quick_bet_frame, text=str(bet), 
                           command=lambda b=bet: self.bet_amount.set(b),
                           bg="#0f3460", fg="white", width=6,
                           font=("Arial", 10), relief="raised")
            btn.pack(side="left", padx=3)
        
        # Область игры (динамическая)
        self.game_area = tk.Frame(right_frame, bg="#16213e", height=200)
        self.game_area.pack(fill="both", expand=True, pady=(10, 0))
        self.game_area.pack_propagate(False)
        
        # Кнопка "Играть" (будет создаваться динамически)
        self.play_button_frame = tk.Frame(right_frame, bg="#1a1a2e", height=70)
        self.play_button_frame.pack(fill="x", pady=(15, 0))
        
        # Область результатов - ПОСЕРЕДИНЕ И ПОД ИГРОЙ
        self.result_frame = tk.Frame(main_container, bg="#0f3460", 
                                    height=120, relief="ridge", bd=3)
        self.result_frame.pack(fill="x", pady=(10, 0))
        self.result_frame.pack_propagate(False)
        
        self.result_text = tk.Text(self.result_frame, height=5, 
                                  font=("Arial", 12, "bold"), 
                                  bg="#0f3460", fg="#ffffff",
                                  relief="flat", wrap="word",
                                  state="disabled")
        self.result_text.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Статус бар
        self.status_bar = tk.Label(main_container, 
                                  text="Добро пожаловать в Casino! Выберите игру и проиграйте квартиру.", 
                                  bg="#16213e", fg="#00b4d8", 
                                  font=("Arial", 10, "italic"),
                                  relief="sunken", bd=1)
        self.status_bar.pack(side="bottom", fill="x", pady=(10, 0))
        
        # Инициализация
        self.clear_game_area()
        self.update_balance_display()
    
    def clear_game_area(self):
        """Очищает область игры"""
        for widget in self.game_area.winfo_children():
            widget.destroy()
        self.slot_labels = []  # Очищаем список ярлыков
        
        # Скрываем кнопку "Играть"
        if self.game_play_button:
            self.game_play_button.pack_forget()
    
    def show_play_button(self, command):
        """Показывает кнопку 'Играть'"""
        # Очищаем фрейм кнопки
        for widget in self.play_button_frame.winfo_children():
            widget.destroy()
        
        # Создаем новую кнопку
        self.game_play_button = tk.Button(self.play_button_frame, 
                                         text="🎮 ИГРАТЬ 🎮", 
                                         command=command,
                                         font=("Arial", 16, "bold"),
                                         bg="#00b894", fg="white",
                                         activebackground="#00a085",
                                         width=20, height=2,
                                         relief="raised", bd=4)
        self.game_play_button.pack()
    
    def update_balance_display(self):
        """Обновляет отображение баланса"""
        color = "#00b894" if self.balance >= 1000 else "#ff7675"
        self.balance_label.config(text=f"💰 БАЛАНС: {self.balance} ₽", fg=color)
        
        # Отключаем кнопки если баланс низкий
        state = "normal" if self.balance > 0 else "disabled"
        for btn in [self.coin_button, self.dice_button, self.slots_button]:
            btn.config(state=state)
    
    def show_result(self, message, is_win=True):
        """Показывает результат с цветом"""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        
        # Устанавливаем цвет текста
        if "проиграли" in message.lower() or "мимо" in message.lower() or "не угадал" in message.lower():
            bg_color = "#d63031"  # Красный для проигрыша
            fg_color = "#ffffff"
            self.result_text.config(bg=bg_color, fg=fg_color)
        else:
            bg_color = "#00b894"  # Зеленый для выигрыша
            fg_color = "#ffffff"
            self.result_text.config(bg=bg_color, fg=fg_color)
        
        self.result_text.insert(1.0, message)
        self.result_text.config(state="disabled")
        
        # Обновляем статус бар
        short_msg = message.split("\n")[0]
        self.status_bar.config(text=short_msg)
    
    def validate_bet(self):
        """Проверяет корректность ставки"""
        bet = self.bet_amount.get()
        if bet <= 0:
            messagebox.showerror("Ошибка", "Ставка должна быть больше 0!")
            return False
        if bet > self.balance:
            messagebox.showerror("Ошибка", f"Недостаточно средств! Ваш баланс: {self.balance}")
            return False
        return True
    
    def setup_coin_flip(self):
        """Настройка интерфейса для Coin Flip"""
        self.clear_game_area()
        self.current_game = "coin"
        
        # Заголовок игры
        title = tk.Label(self.game_area, text="🪙 COIN FLIP", 
                        font=("Arial", 16, "bold"),
                        bg="#16213e", fg="#3498db")
        title.pack(pady=10)
        
        # Описание
        desc = tk.Label(self.game_area, 
                       text="Выберите сторону монеты:", 
                       font=("Arial", 12),
                       bg="#16213e", fg="#ffffff")
        desc.pack(pady=5)
        
        # Выбор стороны
        choice_frame = tk.Frame(self.game_area, bg="#16213e")
        choice_frame.pack(pady=15)
        
        self.choice_var = tk.StringVar(value="h")
        
        # Стили для радио-кнопок
        radio_style = {"font": ("Arial", 12), "bg": "#16213e", 
                      "fg": "#ffffff", "selectcolor": "#0f3460"}
        
        tk.Radiobutton(choice_frame, text="ОРЁЛ", 
                      variable=self.choice_var, 
                      value="h", **radio_style).pack(side="left", padx=20)
        
        tk.Radiobutton(choice_frame, text="РЕШКА", 
                      variable=self.choice_var, 
                      value="t", **radio_style).pack(side="left", padx=20)
        
        # Показываем кнопку "Играть"
        self.show_play_button(self.play_coin_flip)
        
        self.status_bar.config(text="Выбрана игра: Coin Flip. Сделайте ставку и выберите сторону монеты.")
    
    def setup_dice(self):
        """Настройка интерфейса для Dice"""
        self.clear_game_area()
        self.current_game = "dice"
        
        # Заголовок игры
        title = tk.Label(self.game_area, text="🎲 DICE GAME", 
                        font=("Arial", 16, "bold"),
                        bg="#16213e", fg="#9b59b6")
        title.pack(pady=10)
        
        # Описание
        desc = tk.Label(self.game_area, 
                       text="Угадайте число от 1 до 6:", 
                       font=("Arial", 12),
                       bg="#16213e", fg="#ffffff")
        desc.pack(pady=5)
        
        # Выбор числа
        number_frame = tk.Frame(self.game_area, bg="#16213e")
        number_frame.pack(pady=15)
        
        self.dice_var = tk.IntVar(value=1)
        
        # Большие кнопки для выбора числа
        for i in range(1, 7):
            btn = tk.Button(number_frame, text=str(i), 
                           command=lambda num=i: self.dice_var.set(num),
                           font=("Arial", 14, "bold"),
                           bg="#0f3460", fg="#ffffff",
                           width=4, height=2,
                           relief="raised",
                           activebackground="#9b59b6")
            btn.pack(side="left", padx=5)
        
        # Показываем кнопку "Играть"
        self.show_play_button(self.play_dice)
        
        self.status_bar.config(text="Выбрана игра: Dice. Сделайте ставку и выберите число от 1 до 6.")
    
    def setup_slots(self):
        """Настройка интерфейса для Slots"""
        self.clear_game_area()
        self.current_game = "slots"
        
        # Заголовок игры
        title = tk.Label(self.game_area, text="🎰 SLOT MACHINE", 
                        font=("Arial", 16, "bold"),
                        bg="#16213e", fg="#e74c3c")
        title.pack(pady=10)
        
        # Описание правил
        rules_frame = tk.Frame(self.game_area, bg="#16213e")
        rules_frame.pack(pady=10)
        
        rules_text = """🎯 Правила:
• 3 одинаковых = Джекпот x10
• 2 одинаковых = Выигрыш x2
• Все разные = Проигрыш"""
        
        rules_label = tk.Label(rules_frame, text=rules_text,
                              font=("Arial", 10),
                              bg="#16213e", fg="#ffffff",
                              justify="left")
        rules_label.pack()
        
        # Создаем фрейм для слотов
        self.slots_display_frame = tk.Frame(self.game_area, bg="#16213e")
        self.slots_display_frame.pack(pady=10)
        
        # Инициализируем слоты с пустыми значениями
        self.initialize_slots_display()
        
        # Показываем кнопку "Играть"
        self.show_play_button(self.play_slots)
        
        self.status_bar.config(text="Выбрана игра: Slots. Сделайте ставку и нажмите 'Играть'!")
    
    def initialize_slots_display(self):
        """Инициализирует дисплей слотов"""
        self.slot_labels = []
        for i in range(3):
            label = tk.Label(self.slots_display_frame, text="❓", 
                            font=("Arial", 48, "bold"), 
                            bg="#0f3460", fg="#ffffff",
                            width=3, height=1,
                            relief="ridge", bd=4)
            label.pack(side="left", padx=10)
            self.slot_labels.append(label)
    
    def update_slot_display(self, symbols):
        """Обновляет дисплей слотов с заданными символами и цветами"""
        for i, symbol in enumerate(symbols):
            emoji = symbol["emoji"] if isinstance(symbol, dict) else symbol
            color = self.get_symbol_color(emoji)
            self.slot_labels[i].config(text=emoji, fg=color)
    
    def play_coin_flip(self):
        """Игра Coin Flip"""
        if not self.validate_bet():
            return
        
        bet = self.bet_amount.get()
        choice = self.choice_var.get()
        
        # Анимация подбрасывания
        self.show_result("Подбрасываем монетку...\n\n⚪", False)
        self.root.update()
        
        # Анимация
        for _ in range(5):
            self.show_result("Подбрасываем монетку...\n\n🔄", False)
            self.root.update()
            time.sleep(0.2)
        
        result = random.choice(["h", "t"])
        result_text = "ОРЁЛ" if result == "h" else "РЕШКА"
        
        time.sleep(0.5)
        
        # Определяем результат
        if choice == result:
            win_amount = bet
            self.balance += win_amount
            message = f"🎉 ВЫ ВЫИГРАЛИ!\n\nВыпало: {result_text}\nСтавка: {bet} ₽\nВыигрыш: +{win_amount} ₽\nНовый баланс: {self.balance} ₽"
            update_stats(bet, win_amount)
            is_win = True
        else:
            self.balance -= bet
            message = f"😢 ВЫ ПРОИГРАЛИ\n\nВыпало: {result_text}\nСтавка: {bet} ₽\nПотеря: -{bet} ₽\nНовый баланс: {self.balance} ₽"
            update_stats(bet, -bet)
            is_win = False
        
        self.show_result(message, is_win)
        self.update_balance_display()
    
    def play_dice(self):
        """Игра Dice"""
        if not self.validate_bet():
            return
        
        bet = self.bet_amount.get()
        guess = self.dice_var.get()
        
        # Анимация броска
        self.show_result("Бросаем кости...\n\n🎲", False)
        self.root.update()
        
        # Анимация вращения
        for _ in range(8):
            random_num = random.randint(1, 6)
            self.show_result(f"Бросаем кости...\n\n🎲 {random_num}", False)
            self.root.update()
            time.sleep(0.15)
        
        roll = random.randint(1, 6)
        
        time.sleep(0.5)
        
        # Определяем результат
        if guess == roll:
            win_amount = bet * 5
            self.balance += win_amount
            message = f"🔥 ДЖЕКПОТ! x5\n\nВаше число: {guess}\nВыпало: {roll}\nСтавка: {bet} ₽\nВыигрыш: +{win_amount} ₽\nНовый баланс: {self.balance} ₽"
            update_stats(bet, win_amount)
            is_win = True
        else:
            self.balance -= bet
            message = f"❌ НЕ УГАДАЛИ\n\nВаше число: {guess}\nВыпало: {roll}\nСтавка: {bet} ₽\nПотеря: -{bet} ₽\nНовый баланс: {self.balance} ₽"
            update_stats(bet, -bet)
            is_win = False
        
        self.show_result(message, is_win)
        self.update_balance_display()
    
    def play_slots(self):
        """Игра Slots"""
        if not self.validate_bet():
            return
        
        bet = self.bet_amount.get()
        
        self.show_result("Крутим слоты...\n\n🎰", False)
        self.root.update()
        
        # Анимация вращения
        spins = 15
        for spin in range(spins):
            # Генерируем случайные символы для анимации
            temp_symbols = []
            for _ in range(3):
                symbol_data = random.choice(self.symbols)
                temp_symbols.append(symbol_data)
            
            # Обновляем дисплей с цветами
            self.update_slot_display(temp_symbols)
            
            # Замедляем вращение в конце
            delay = 0.05 + (spin / spins) * 0.15
            self.root.update()
            time.sleep(delay)
        
        # Финальный результат
        reel = [random.choice(self.symbols) for _ in range(3)]
        
        # Обновляем дисплей с финальными символами
        self.update_slot_display(reel)
        
        time.sleep(0.5)
        
        # Получаем эмодзи для отображения в результате
        reel_emojis = [symbol["emoji"] for symbol in reel]
        reel_names = [self.get_symbol_name(emoji) for emoji in reel_emojis]
        
        # Определяем результат
        if len(set(reel_emojis)) == 1:  # Все три одинаковые
            win_amount = bet * 10
            self.balance += win_amount
            message = f"💎💎💎 MEGA WIN! x10\n\nСимволы: {' | '.join(reel_emojis)}\n({', '.join(reel_names)})\nСтавка: {bet} ₽\nВыигрыш: +{win_amount} ₽\nНовый баланс: {self.balance} ₽"
            update_stats(bet, win_amount)
            is_win = True
        elif len(set(reel_emojis)) == 2:  # Два одинаковых
            win_amount = bet * 2
            self.balance += win_amount
            message = f"✨ ВЫИГРЫШ! x2\n\nСимволы: {' | '.join(reel_emojis)}\n({', '.join(reel_names)})\nСтавка: {bet} ₽\nВыигрыш: +{win_amount} ₽\nНовый баланс: {self.balance} ₽"
            update_stats(bet, win_amount)
            is_win = True
        else:  # Все разные
            self.balance -= bet
            message = f"😢 МИМО\n\nСимволы: {' | '.join(reel_emojis)}\n({', '.join(reel_names)})\nСтавка: {bet} ₽\nПотеря: -{bet} ₽\nНовый баланс: {self.balance} ₽"
            update_stats(bet, -bet)
            is_win = False
        
        self.show_result(message, is_win)
        self.update_balance_display()
    
    def show_stats_gui(self):
        """Показывает статистику"""
        stats_text = show_stats()
        
        # Создаем отдельное окно для статистики
        stats_window = tk.Toplevel(self.root)
        stats_window.title("📊 Статистика")
        stats_window.geometry("400x350")
        stats_window.configure(bg="#16213e")
        stats_window.resizable(False, False)
        
        # Центрируем окно
        stats_window.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.root.winfo_screenheight() // 2) - (350 // 2)
        stats_window.geometry(f'400x350+{x}+{y}')
        
        # Заголовок
        title = tk.Label(stats_window, text="📊 СТАТИСТИКА ИГРЫ", 
                        font=("Arial", 18, "bold"),
                        bg="#16213e", fg="#00b4d8")
        title.pack(pady=20)
        
        # Текст статистики
        stats_label = tk.Label(stats_window, text=stats_text,
                              font=("Courier", 12),
                              bg="#0f3460", fg="#ffffff",
                              justify="left", relief="ridge", bd=2)
        stats_label.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Кнопка закрытия
        close_btn = tk.Button(stats_window, text="Закрыть",
                             command=stats_window.destroy,
                             font=("Arial", 12, "bold"),
                             bg="#e74c3c", fg="white",
                             width=15, height=2)
        close_btn.pack(pady=10)

def casino_gui():
    """Запуск графического интерфейса"""
    root = tk.Tk()
    app = CasinoGUI(root)
    root.mainloop()

# ---------- Main ----------
if __name__ == "__main__":
    casino_gui()