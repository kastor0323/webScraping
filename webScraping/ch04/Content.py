class Content:
    """
    글/페이지 전체에 사용할 시반 클래스
    """

    def __init__(self, topic, url, title, body):
        self.topic = topic
        self.title = title
        self.body = body
        self.url = url

    def print(self):
        """
        출력 결과를 원하는 대로 바꿀 수 있는 함수
        """
        print("New article found for topic {}".format(self.topic))
        print('URL: {}'.format(self.url))
        print('Title: {}'.format(self.title))
        print('Body: {}'.format(self.body))

