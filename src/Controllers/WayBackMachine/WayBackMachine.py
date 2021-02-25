from src.Controllers.ServerResponse.ServerResponse import ServerResponse


class WayBackMachine:
    def __init__(self):
        self._search_url = "http://web.archive.org/cdx/search/cdx"
        self._session = ServerResponse(user_agent="waybackpack")
        self._bad_status_code = [400, 403, 404, 408, 429, 500, 503]

    def search_snapshots(self, url: str):
        url = f"https://web.archive.org/cdx/search/cdx?url={url}&showDupeCount=true&output=json"
        cdx = self._session.get(url).json()

        if cdx is None:
            return []

        if len(cdx) < 2:
            return []

        fields = cdx[0]
        snapshots = [dict(zip(fields, row)) for row in cdx[1:]]
        snapshots_temp = []

        for snapshot in snapshots:
            try:
                status_code = int(snapshot['statuscode'])
            except ValueError:
                continue

            if status_code in self._bad_status_code:
                continue

            snapshots_temp.append(snapshot)

        timestamps = [(snap["timestamp"], snap['statuscode']) for snap in snapshots_temp]

        return timestamps
