import asyncio
import aiohttp


URL = "https://raw.githubusercontent.com/avito-tech/python-trainee-assignment/main/matrix.txt"


async def fetch_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
            else:
                print(f"Ошибка: {response.status}")
                return None


def parse_matrix(data):
    matrix = []
    for line in data.split('\n'):
        if line.startswith('|'):
            row = [int(num) for num in line.split('|')[1:-1] if num.strip()]
            matrix.append(row)
    return matrix


def get_list(matrix):
    if not matrix or not matrix[0]:
        return []

    res = []
    left, right = 0, len(matrix[0]) - 1
    top, bottom = 0, len(matrix) - 1

    while left <= right and top <= bottom:
        # левый столбец
        res.extend(matrix[row][left] for row in range(top, bottom + 1))
        left += 1
        if left > right:
            break

        # нижняя строка
        res.extend(matrix[bottom][col] for col in range(left, right + 1))
        bottom -= 1
        if top > bottom:
            break

        # правый столбец
        res.extend(matrix[row][right] for row in range(bottom, top - 1, -1))
        right -= 1
        if left > right:
            break

        # верхняя строка
        res.extend(matrix[top][col] for col in range(right, left - 1, -1))
        top += 1

    return res


async def main():
    data = await fetch_data(URL)
    if data:
        matrix = parse_matrix(data)
        res = get_list(matrix)
        print(res)

asyncio.run(main())