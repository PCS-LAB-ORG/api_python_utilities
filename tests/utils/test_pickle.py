from apu.utils import pickle


def test():
    # Usage

    from pathlib import Path

    script_dir = Path(__file__).parent
    pickle_file = f"{script_dir}/secure.pkl"

    my_data = {"id": 42, "sensitive": "top-secret"}
    pickle.sign_and_pickle(my_data, pickle_file)

    try:
        loaded = pickle.verify_and_unpickle(pickle_file)
        print("Data loaded securely:", loaded)
        assert loaded["id"] == 42
    except ValueError as e:
        print(e)
