def return_list_free_date_and_time_order():
    # Получаем все существующие заказы
    cart_items = CartItem.objects.all()
    # Создаем словарь, где ключ - дата, а значение - список занятых временных интервалов
    occupied_slots = {}
    for item in cart_items:
        date = item.order_day
        time = item.order_time
        if date not in occupied_slots:
            occupied_slots[date] = []
        occupied_slots[date].append(time)

def generated_list_free_date_and_time():
    # Генерируем список доступных дат и времени
    available_dates = []
    start_date = datetime.now().date()
    end_date = start_date + timedelta(days=7)  # Ограничиваем диапазон на 7 дней
    while start_date <= end_date:
        available_times = ['08:00', '09:00', '10:00', '11:00',
                           '12:00', '13:00', '14:00', '15:00',
                           '16:00', '17:00', '18:00', '19:00',]
        if start_date not in occupied_slots:
            available_dates.append((start_date, available_times))
        else:
            occupied_times = occupied_slots[start_date]
            for time in available_times:
                if time not in occupied_times:
                    available_dates.append((start_date, [time]))
        start_date += timedelta(days=1)
    return available_dates