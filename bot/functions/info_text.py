from redis_dict import RedisDict


async def basket_data(redisdict):
    sum = 0
    text = "🛒 Savat "
    for num, book in enumerate((redisdict.values()), 1):
        price = int(book.get("count")) * int(book.get("price"))
        str = f"""
{num}. {book.get('title').strip()}
{book.get("count")} x {book.get("price")} = {price} """
        text += str
        sum += price
    text += f"Jami: {sum}"
    return text


def book_data(book):
    text = f"""🔹Nomi: {book.name.strip()}
Muallifi: {book.author.strip()}
Janri: {book.genre.strip()}
Tarjimon: {book.translater.strip()}
Bet: {book.page_count}
Muqova: {book.cover}
Kitob haqida:
💸 Narxi: {book.price}"""
    return text


async def create_basket(user_id):
    return RedisDict(f"{user_id}")
