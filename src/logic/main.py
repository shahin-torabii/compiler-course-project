from os import walk
from Extractor import *
import zipfile

__projectName = "input"


# def main(zip_path: str):
def main():
    executor = Extractor(getFilePaths(), __projectName)
    executor.executeFiles()


# def getFilePaths(zip_path: str):
def getFilePaths():
    print("Loading file paths...")
    # destination_path = extractZip(zip_path)
    names = []
    filepaths = []

    final_path = os.path.join(
        os.path.dirname(__file__), "..", "test", __projectName
    )
    # w = walk(f"../test/{__projectName}/main")
    print("Project Path: ", final_path)
    w = walk(final_path)
    for dirpath, dirnames, filenames in w:
        for filename in filenames:
            if filename.endswith(".java"):
                names.append(filename)
                filepaths.append(dirpath)
    print("Loading file paths complete\n")
    return names, filepaths


def extractZip(zip_path: str):
    zip_file_path = zip_path
    destination_dir = os.path.dirname(zip_file_path)

    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(destination_dir)
    return destination_dir


def runTest():
    # print(final_output_with_replaced_classes)
    # pint("-----------------------------------")
    # print("Extracted Variables:", extractor.variables)
    # print("------------------------0------------")
    # print("methods:", extractor.methods)
    # print("-----------------------------------")
    # print("code:\n", finalOutput)
    # print("-----------------------------------")
    # print("Final Output with Replaced Variables:")
    # print(final_output_with_replaced_vars)
    # print("-----------------------------------")
    # print("identifiers:", extractor.identifiers)
    return


if __name__ == "__main__":
    main()
