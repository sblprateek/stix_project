from src.ml.predict_balanced import predict


def main():

    path = input("Enter STIX file path: ")

    results = predict(path)

    print("\n--- RESULTS ---\n")

    for r in results[:10]:
        print(r)


if __name__ == "__main__":
    main()
