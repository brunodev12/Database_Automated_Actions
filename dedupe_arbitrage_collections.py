from collections import defaultdict

from connection.conn import client, ARBITRAGE_COLLECTION_KEY_FIELDS

DATABASE_NAME = "Arbitrage_Bidding_Bot"
COLLECTION_NAME = "Collection_Info"


def dedupe_arbitrage_collections(dry_run: bool = True):

    database = client[DATABASE_NAME]
    collection = database[COLLECTION_NAME]

    docs = list(collection.find({}))

    groups = defaultdict(list)
    for doc in docs:
        key = tuple(doc.get(field, "") for field in ARBITRAGE_COLLECTION_KEY_FIELDS)
        groups[key].append(doc)

    ids_to_delete = []
    for key, group in groups.items():
        if len(group) <= 1:
            continue

        group.sort(key=lambda d: d.get("last_update_db", ""), reverse=True)
        keep, duplicates = group[0], group[1:]

        print("-------------------------Duplicate group-------------------------")
        print(key)
        print(f"Keeping _id={keep['_id']} (last_update_db={keep.get('last_update_db')})")
        for dup in duplicates:
            print(f"Deleting _id={dup['_id']} (last_update_db={dup.get('last_update_db')})")
            ids_to_delete.append(dup["_id"])

    print("====================================================================")
    print(f"Total documents: {len(docs)}")
    print(f"Duplicate groups: {sum(1 for g in groups.values() if len(g) > 1)}")
    print(f"Documents to delete: {len(ids_to_delete)}")

    if dry_run:
        print("Dry run: no documents were deleted. Re-run with dry_run=False to apply.")
        return

    if ids_to_delete:
        result = collection.delete_many({"_id": {"$in": ids_to_delete}})
        print(f"Deleted {result.deleted_count} duplicate documents.")


if __name__ == '__main__':

    dedupe_arbitrage_collections(dry_run=False)
