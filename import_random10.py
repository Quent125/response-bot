# 匯入unidecode模組
from unidecode import unidecode

import random
import json
import os



# 獲取當前.py檔案的路徑
current_directory = os.path.dirname(os.path.abspath(__file__))
json_file_path = os.path.join(current_directory, 'restaurant_data.json')

# 檔案路徑
json_file_path = 'restaurant_data.json'

# 讀取JSON檔案內容


def load_from_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}


# 檢查是否存在相符的.json檔案，並讀取它作為程式的database
if os.path.isfile(json_file_path):
    print('*********************')
    print(f'找到相符的.json檔案：{json_file_path}')
    database = load_from_json(json_file_path)
else:
    print('*********************')
    print('在當前目錄中找不到相符的.json檔案，將使用空的.json檔案做為新的database。')
    database = {}

# 寫入資料到JSON檔案，並備份目標檔案


def write_to_json_with_backup(data, file_path):
    # 建立備份目標檔案的名稱
    backup_file_path = create_backup_file_path(file_path)

    # 備份目標檔案（如果存在）
    if os.path.isfile(file_path):
        os.rename(file_path, backup_file_path)

    # 寫入新資料到JSON檔案
    with open(file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=4)

    print(f'資料已成功寫入 {file_path}，同時已備份為 {backup_file_path}')

# 建立備份檔案的名稱


def create_backup_file_path(original_file_path):
    base_name, ext = os.path.splitext(original_file_path)
    directory = os.path.dirname(original_file_path)
    counter = 1
    while True:
        backup_file_path = f'{base_name} ({counter:02d}){ext}'
        if not os.path.isfile(os.path.join(directory, backup_file_path)):
            return os.path.join(directory, backup_file_path)
        counter += 1


# 初始化database，讀取外部JSON檔案
database = load_from_json(json_file_path)

# 新增餐廳資料


def add_new_restaurant(database):
    restaurant_name = input('請輸入新餐廳的名稱：')
    address = input('請輸入新餐廳的地址：')
    items = input('請輸入新餐廳提供的商品（以逗號分隔）：').split(',')
    price = (input('請輸入新餐廳的價位：'))
    business_hours = (input('請輸入新餐廳的營業時間：')).split(',')
    category = input('請輸入新餐廳的分類：')
    keyword = input('請輸入新餐廳的關鍵字（以逗號分隔）：').split(',')

    new_restaurant = {
        '店名': restaurant_name,
        '地址': address,
        '商品': items,
        '價位': price,
        '營業時間': business_hours,
        '分類': category,
        '關鍵字': keyword,
        '評價': []  # 初始化評價為空列表
    }
    database[restaurant_name] = new_restaurant
    print('已成功新增餐廳：{}'.format(restaurant_name))
    write_to_json_with_backup(database, json_file_path)  # 寫入JSON 檔案

# 依關鍵字尋找餐廳


def find_restaurants_by_keyword(keyword, database):
    matching_restaurants = []
    for restaurant_name, restaurant in database.items():
        keywords = restaurant.get('關鍵字', [])
        for kw in keywords:
            if keyword in kw:
                matching_restaurants.append(restaurant)
                break  # 一旦找到一個符合的關鍵字，就不再檢查其他關鍵字
    return matching_restaurants


# 顯示特定店名的餐廳資訊 (讀取外部JSON檔案)
def display_restaurant_info_by_name_from_json(restaurant_name, json_file_path):
    database = load_from_json(json_file_path)
    matching_restaurant = None

    # 將輸入的店名轉換為中文拼音輸入法
    restaurant_name_in_pinyin = unidecode(restaurant_name)

    for name, restaurant in database.items():
        # 將存儲的店名轉換為中文拼音進行比較
        name_in_pinyin = unidecode(restaurant['店名'])
        if name_in_pinyin == restaurant_name_in_pinyin:
            matching_restaurant = restaurant
            break

    if matching_restaurant:
        print('店名：{}'.format(matching_restaurant['店名']))
        print('地址：{}'.format(matching_restaurant['地址']))
        print('商品：{}'.format(matching_restaurant['商品']))
        print('價位：{}'.format(matching_restaurant['價位']))
        print('營業時間：{}'.format(matching_restaurant['營業時間']))
        print('分類：{}'.format(matching_restaurant['分類']))

        # 顯示評價（如果有評價）
        if '評價' in matching_restaurant and matching_restaurant['評價']:
            random_review = random.choice(matching_restaurant['評價'])
            print('隨機評價：{}'.format(random_review))
        else:
            print('目前還沒有評價。')
    else:
        print('找不到名稱為 {} 的餐廳。'.format(restaurant_name))


# 隨機選擇餐廳
def get_random_restaurant(restaurants):
    if restaurants:
        return random.choice(restaurants)
    return None

# 新增商品


def add_items_to_restaurant(database):
    restaurant_name = input('請輸入想要新增商品的餐廳名稱：')
    restaurant_name_in_pinyin = unidecode(restaurant_name).lower()

    for name, restaurant in database.items():
        restaurant_name_in_pinyin = unidecode(
            restaurant['店名'].replace(" ", "")).lower()
        if restaurant_name_in_pinyin in database:
            items = input('請輸入想要新增的商品（以逗號分隔，按Enter結束）：').split(',')
            database[restaurant_name_in_pinyin]['商品'].extend(items)
            print('已成功新增商品到 {} 餐廳：{}'.format(restaurant_name_in_pinyin, items))
            write_to_json_with_backup(database, json_file_path)
    else:
        print('找不到名稱為 {} 的餐廳。'.format(restaurant_name_in_pinyin))

# 新增評價


def add_review(database, restaurant_name):
    review = input('請輸入對 {} 的評價（30字以內）：'.format(restaurant_name))
    if len(review) <= 30:
        restaurant = database.get(restaurant_name)
        if restaurant:
            if '評價' in restaurant:
                restaurant['評價'].append(review)
            else:
                restaurant['評價'] = [review]
            print('評價已成功新增。')
            write_to_json_with_backup(database, json_file_path)
        else:
            print('找不到名稱為 {} 的餐廳。'.format(restaurant_name))
    else:
        print('評價必須在30字以內。')

# 顯示隨機評價


def display_random_review(database, restaurant_name):
    restaurant = database.get(restaurant_name)
    if restaurant and '評價' in restaurant:
        reviews = restaurant['評價']
        if reviews:
            random_review = random.choice(reviews)
            print('隨機評價：{}'.format(random_review))
        else:
            print('目前還沒有評價。')
    else:
        print('找不到名稱為 {} 的餐廳或該餐廳沒有評價。'.format(restaurant_name))


# 主程式
def main():
    while True:
        print('*********************')
        print('歡迎使用，我可以透過您輸入的資料進行不同的回應')
        print('輸入指定的分類(如"早餐"等)，我會列出含有關鍵字的店家')
        print('輸入指令-「店名」後，我可以列出此店家的詳細資料。')
        print('輸入指令-「新增」後，使用者可以自行新增店家的資訊')
        print('輸入指令-「隨機」後，我會直接隨機挑選一間店家')
        print('輸入指令-「評價」後，可以對指定的店家進行評價')
        print('輸入指令-「離開」後，程式會直接關閉')
        user_input = input('現在，請輸入您的問題或指令：')
        if user_input == '離開':
            break
        elif user_input == '隨機':
            if database:
                random_choice = random.choice(list(database.keys()))
                restaurant = database[random_choice]
                print('********************')
                print('我建議您可以去-{}'.format(restaurant['店名']))
                print('他們在-{}'.format(restaurant['地址']))
                print('他們提供的商品有：{}'.format(restaurant['商品']))
                print('價位：{}'.format(restaurant['價位']))
                print('營業時間：{}'.format(restaurant['營業時間']))
                print('分類：{}'.format(restaurant['分類']))
                print('')

                # 檢查是否有評價
                if '評價' in restaurant and restaurant['評價']:
                    random_review = random.choice(restaurant['評價'])
                    print('用戶評價：{}'.format(random_review))
                else:
                    print('此餐廳尚無評價。')

                # 詢問用戶是否要對此餐廳進行評價
                review_choice = input('是否要對此餐廳進行評價？（是/否）：')
                if review_choice.lower() == '是':
                    add_review(database, random_choice)  # 評價餐廳
                elif review_choice.lower() == '否':
                    continue  # 回到主程式
                else:
                    print('請輸入有效的選項（是/否）。')
                    write_to_json_with_backup(
                        database, json_file_path)  # 在新增或更新資料時，使用新的寫入函數
            else:
                print('在資料庫中找不到餐廳。')

        elif user_input == '新增':  # 使用者新增一間店家
            add_new_restaurant(database)
            write_to_json_with_backup(
                database, json_file_path)  # 在新增或更新資料時，使用新的寫入函數
        elif user_input == '增加商品':
            add_items_to_restaurant(database)

        elif user_input == '店名':  # 搜尋店名獲得店家的詳細資訊
            name_input = input('請輸入要查詢的店名：')
            display_restaurant_info_by_name_from_json(
                name_input, json_file_path)

        elif user_input == '評價':  # 主程式中新增評價和顯示隨機評價的選項
            name_input = input('請輸入要評價的餐廳名稱：')
            add_review(database, name_input)
            write_to_json_with_backup(
                database, json_file_path)  # 在新增或更新資料時，使用新的寫入函數
        elif user_input == '隨機評價':
            name_input = input('請輸入要查詢評價的餐廳名稱：')
            display_random_review(database, name_input)

        else:
            restaurants = find_restaurants_by_keyword(user_input, database)
            if restaurants:
                random_restaurant = get_random_restaurant(restaurants)
                print('*********************')
                print('店名:{}'.format(random_restaurant['店名']))
                print('地址:{}'.format(random_restaurant['地址']))
                print('提供的商品有：{}'.format(random_restaurant['商品']))
                print('價位：{}'.format(random_restaurant['價位']))
                print('營業時間：{}'.format(random_restaurant['營業時間']))
                print('分類：{}'.format(random_restaurant['分類']))
                print('')

            else:
                print('抱歉，我不知道該如何回答您的問題，請再次檢查輸入的指令格式是否正確。')


if __name__ == '__main__':
    main()
