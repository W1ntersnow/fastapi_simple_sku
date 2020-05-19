import pytest
import db.models as models


@pytest.mark.parametrize('input_data', [
    {
        "title": "test_item1",
        "description": "test_item1_desc",
        "sku": "unit",
        "type_id": 0,
        "balance": 5,
    },
])
def test_create_item(input_data, client, db):
    response = client.post(
        "/v1/item/",
        json=input_data,
    )
    assert response.status_code == 200

    res_json = response.json()

    for key, value in input_data.items():
        assert res_json[key] == value

    assert 'id' in res_json

    row_id = res_json['id']

    db_row = db.query(models.Item).filter(models.Item.id == row_id).first()
    assert db_row is not None

    db.query(models.Item).delete()
    db.commit()


@pytest.mark.parametrize('input_data', [
    {
        "title": "test_item1",
        "description": "test_item1_desc",
        "sku": "unit",
        "type_id": 0,
        "balance": 5,
    },
])
def test_delete_item(input_data, client, db):
    response = client.post(
        "/v1/item/",
        json=input_data,
    )
    assert response.status_code == 200

    res_json = response.json()

    for key, value in input_data.items():
        assert res_json[key] == value

    assert 'id' in res_json

    row_id = res_json['id']

    db_row = db.query(models.Item).filter(models.Item.id == row_id).first()
    assert db_row is not None

    response = client.delete(
        f"/v1/item/{row_id}",
    )
    assert response.status_code == 200

    db_row = db.query(models.Item).filter(models.Item.id == row_id).first()
    assert db_row is None

    db.query(models.Item).delete()
    db.commit()


@pytest.mark.parametrize('input_data', [
    (
        [
            {
                "title": "test_item1",
                "description": "test_item1_desc",
                "sku": "unit",
                "type_id": 1,
                "balance": 5
            },
            {
                "title": "test_item2",
                "description": "test_item2_desc",
                "sku": "unit",
                "type_id": 2,
                "balance": 4
            }
        ]
    ),
])
def test_items_filter(input_data, client, db):
    types_ids = []
    items_ids = []
    for data in input_data:
        type_number = data["type_id"]
        response = client.post(
            "/v1/item_type/",
            json={
                'title': f'test{type_number}',
                'description': f'test_desc{type_number}',
            },
        )
        type_id = response.json()['id']
        types_ids.append(type_id)
        data['type_id'] = type_id
        response = client.post(
            "/v1/item/",
            json=data,
        )
        items_ids.append(response.json()['id'])

    response = client.get("/v1/item/")
    assert len(response.json()) == len(input_data)

    for item_type in types_ids:
        response = client.get(f"/v1/item/?item_type={item_type}")

        for row in response.json():
            assert row['type_id'] == item_type

    db.query(models.ItemType).delete()
    db.query(models.Item).delete()
    db.commit()


@pytest.mark.parametrize('input_data, new_balance', [
    (
        {
            "title": "test_item1",
            "description": "test_item1_desc",
            "sku": "unit",
            "type_id": 0,
            "balance": 5
        },
        10,
    ),
])
def test_item_balance_change(input_data, new_balance, client, db):
    response = client.post(
        "/v1/item/",
        json=input_data,
    )
    row_id = response.json()['id']

    db_row = db.query(models.Item).filter(models.Item.id == row_id).first()

    assert input_data['balance'] == db_row.balance

    response = client.patch(
        f"/v1/item/{row_id}/balance",
        json={'balance': new_balance}
    )
    assert response.status_code == 200
    updated_balance = response.json()['balance']
    assert updated_balance == new_balance

    db.commit()
    db_row = db.query(models.Item).filter(models.Item.id == row_id).first()
    assert new_balance == db_row.balance

    db.query(models.Item).delete()
    db.commit()
