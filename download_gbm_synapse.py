"""
Download the adult BraTS-GLI dataset from Synapse into data/BraTS-GLI/.
Provide the token via the SYNAPSE_AUTH_TOKEN env var, or omit to log in
interactively:

  export SYNAPSE_AUTH_TOKEN=xxxxxxxx
  python download_gbm_synapse.py
"""
import os
import synapseclient
import synapseutils

BASE       = os.path.dirname(os.path.abspath(__file__))
DEST       = os.path.join(BASE, "data", "BraTS-GLI")
SYNAPSE_ID = os.environ.get("SYNAPSE_GLI_ID", "syn51156910")

os.makedirs(DEST, exist_ok=True)


def main():
    syn = synapseclient.Synapse()

    token = os.environ.get("SYNAPSE_AUTH_TOKEN")
    if token:
        syn.login(authToken=token)
    else:
        syn.login()

    # remove_from_download_list is capped at 1000 entries per call
    _original_remove = syn.remove_from_download_list

    def _chunked_remove(list_of_files, **kwargs):
        for i in range(0, len(list_of_files), 1000):
            _original_remove(list_of_files=list_of_files[i:i + 1000], **kwargs)

    syn.remove_from_download_list = _chunked_remove

    print(f"Downloading {SYNAPSE_ID} -> {DEST}")
    synapseutils.syncFromSynapse(syn, SYNAPSE_ID, path=DEST)
    print("Download complete.")


if __name__ == "__main__":
    main()
