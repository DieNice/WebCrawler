class UrlsDTO:
    _urls = [str]

    def __init__(self, urls=[]) -> None:
        self._urls = urls

    def add(self, newdata: str) -> None:
        self._urls.append(newdata)

    def __add__(self, other):
        for i in other:
            self._urls.append(i)
        return self

    def __str__(self) -> str:
        res = '-----URLS-----\n'
        for i in self._urls:
            res += i + "\n"
        res += '-----URLS-----\n'
        return res

    def __len__(self) -> int:
        return len(self._urls)

    def __getitem__(self, item) -> None:
        return self._urls[item]

    def append(self, new: str) -> None:
        self._urls.append(new)
