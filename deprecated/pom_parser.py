# import xml.etree.ElementTree as ET
# import os
# import argparse
# import pandas as pd


# class PomVersionFinder:
#     def __init__(self, pom_path):
#         self.namespace = {"mvn": "http://maven.apache.org/POM/4.0.0"}
#         self.pom_path = os.path.abspath(pom_path)
#         self.properties = {}

#     def find_library_version(self, library_name):
#         """
#         Find version of a specific library in the given pom.xml file
#         """
#         try:
#             tree = ET.parse(self.pom_path)
#             root = tree.getroot()
#             # Load properties first
#             self._load_properties(self.pom_path, root)
#             # First check in dependencyManagement
#             version = self._check_dependency_section(
#                 root,
#                 library_name,
#                 ".//mvn:dependencyManagement/mvn:dependencies/mvn:dependency",
#             )

#             # If not found, check in direct dependencies
#             if not version:
#                 version = self._check_dependency_section(
#                     root, library_name, ".//mvn:dependencies/mvn:dependency"
#                 )
#             return version

#         except ET.ParseError as e:
#             print(f"Error parsing POM file: {e}")
#             return None
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             return None

#     def _load_properties(self, pom_path, root):
#         """
#         Load all properties from POM file including parent properties if needed
#         """
#         # First load parent properties if exists
#         parent = root.find("mvn:parent", self.namespace)
#         if parent is not None:
#             parent_path = self._find_parent_pom(pom_path, parent)
#             if parent_path:
#                 parent_tree = ET.parse(parent_path)
#                 parent_root = parent_tree.getroot()
#                 self._load_properties(parent_path, parent_root)

#         # Load project coordinates as properties
#         project_props = {
#             "project.groupId": root.find("mvn:groupId", self.namespace),
#             "project.artifactId": root.find("mvn:artifactId", self.namespace),
#             "project.version": root.find("mvn:version", self.namespace),
#         }

#         for key, elem in project_props.items():
#             if elem is not None:
#                 self.properties[key] = elem.text

#         # Load properties from properties section
#         props_section = root.find("mvn:properties", self.namespace)
#         if props_section is not None:
#             for prop in props_section:
#                 name = prop.tag.split("}")[-1]  # Remove namespace
#                 self.properties[name] = prop.text

#     def _find_parent_pom(self, pom_path, parent_elem):
#         """
#         Find parent POM file relative to current POM
#         """
#         relative_path = parent_elem.find("mvn:relativePath", self.namespace)

#         relative_path = (
#             relative_path.text if relative_path is not None else "../pom.xml"
#         )
#         parent_path = os.path.normpath(
#             os.path.join(os.path.dirname(pom_path), relative_path)
#         )
#         return parent_path if os.path.exists(parent_path) else None

#     def _check_dependency_section(self, root, library_name, xpath):
#         """
#         Check for library in specific dependency section
#         """
#         for dep in root.findall(xpath, self.namespace):
#             group_id = dep.find("mvn:groupId", self.namespace)
#             artifact_id = dep.find("mvn:artifactId", self.namespace)
#             if artifact_id is not None and group_id is not None:
#                 dependency_text = f"{group_id.text}:{artifact_id.text}"
#                 if dependency_text == library_name:
#                     version = dep.find("mvn:version", self.namespace)
#                     if version is not None:
#                         return self._resolve_version(version.text)
#         return None

#     def _resolve_version(self, version_text):
#         """
#         Resolve version from property if needed
#         """
#         if not version_text or not isinstance(version_text, str):
#             return version_text

#         # Handle property reference ${property.name}
#         if version_text.startswith("${") and version_text.endswith("}"):
#             prop_name = version_text[2:-1]
#             return self.properties.get(prop_name, version_text)

#         return version_text

# def find_lib_version(library_name: str, pom_path: str):
#     finder = PomVersionFinder(pom_path)
#     version = finder.find_library_version(library_name)
#     return version

# def main(args):
#     df = pd.read_csv(args.data_file)
#     for _, row in df.iterrows():
#         print(row["repo_name"])
#         lib_pairs = eval(row["migration_info"])["lib_pairs"]
#         for lib_pair in lib_pairs:
#             from_lib = lib_pair["from_lib"]
#             to_lib = lib_pair["to_lib"]
#             from_pom_path = os.path.join(
#                 args.data_storage,
#                 row["id"],
#                 f"ver1__{row['prev_commit']}",
#                 lib_pair["pom_file"],
#             )
#             to_pom_path = os.path.join(
#                 args.data_storage,
#                 row["id"],
#                 f"ver2__{row['end_commit']}",
#                 lib_pair["pom_file"]
#             )
#             from_lib_version = find_lib_version(from_lib, from_pom_path)
#             to_lib_version = find_lib_version(to_lib, to_pom_path)
#             print(from_lib, to_lib)
#             print(lib_pair["pom_file"])
#             print(from_lib_version, to_lib_version)
#         print("=" * 100)
    


# # Example usage
# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-d", "--data-file", dest="data_file")
#     parser.add_argument("-s", "--data-storage", dest="data_storage")
#     args = parser.parse_args()
#     main(args)
