# clarity-prompt

## Usage

```
docker compose build --build-arg userid=$(id -u) --build-arg groupid=$(id -g)
docker compose run -P django /bin/bash
pdm install
pdm run dev
pdm run test
```

## API

API Docs: http://localhost:8000/api/v1/docs

## Normalized vs DeNormalized

During the discussions it came up of doing this prompt in a normalized vs a denormalized fashion and this solution was categorized as denormalized. However, the normalized version of this has about the same amount of repeating data. So it's really a discussion of Relational Data vs Non-Relational. This solution is partly non-relational because of how the conditions are stored.

So what is the difference between the Relational and Non-Relational solutions? Both would have a Typed API, if you're making a good API in my opinion. However, the relational version gives you additional typing at the database level because the database is also checking types instead of just having a JSON Blob. Having a JSON Blob, gives you added flexibility though. And since I got the sense that rules can change often, I like that extra flexibility. With this solution, a change to:

```python
DocumentRule.CONDITIONS = {
  "new": {"date_joined__gt": datetime.datetime(2024, 1, 1)},
  "biz": {"username__startswith": "biz_"},
  "fam2021": {"username__endswith": "_2021"},
}
```

will automatically adjust the validation in the API and allow new rules with custom queries. This requires no database migrations. So while I don't always like squishy data, I do think it could serve a purpose here if flexibility in the rules is needed.
