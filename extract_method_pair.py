import argparse
import pandas as pd
import os
import json


# def main(args):
#     df = pd.read_csv(args.data_file)
#     records = []
#     for _, row in df.iterrows():
#         diff_files = eval(row["diff_files"])
#         for mode in diff_files:
#             if mode in ["Modified", "Renamed-Modified"]:
#                 parsed_prev = os.path.join(
#                     args.parsed_dir, row["repoName"] + "--" + row["prev_commit"]
#                 )
#                 parsed_cur = os.path.join(
#                     args.parsed_dir, row["repoName"] + "--" + row["endCommit"]
#                 )
#                 for item in diff_files[mode]:
#                     if mode == "Modified":
#                         old_file = new_file = item
#                     else:
#                         old_file, new_file, _ = item

#                     parsed_old_file = old_file.replace("/", "--") + ".json"
#                     parsed_new_file = new_file.replace("/", "--") + ".json"
#                     with open(os.path.join(parsed_prev, parsed_old_file), "r") as f:
#                         old_classes = json.load(f)
#                     with open(os.path.join(parsed_cur, parsed_new_file), "r") as f:
#                         new_classes = json.load(f)

#                     for aclass in old_classes:
#                         if aclass["class_mode"] not in ["Modified", "Renamed-Modified"]:
#                             continue
#                         if aclass["class_mode"] == "Modified":
#                             mapped_tree_path = aclass["tree_path"]
#                         else:
#                             mapped_tree_path = aclass["map_tree_path"]

#                         bclass = None
#                         for cls in new_classes:
#                             if cls["tree_path"] == mapped_tree_path:
#                                 bclass = cls
#                         if not bclass:
#                             raise Exception("No mapped class found")

#                         old_methods = aclass["methods"]
#                         new_methods = bclass["methods"]
#                         for method in old_methods:
#                             if method["method_mode"] not in [
#                                 "Modified",
#                                 "Renamed-Modified",
#                             ]:
#                                 continue
#                             if method["method_mode"] == "Modified":
#                                 mapped_sig = (method["name"], method["parameters"])
#                             else:
#                                 mapped_sig = method["map_method"]

#                             bmethod = None
#                             for m in new_methods:
#                                 if compare_sig((m["name"], m["parameters"]), mapped_sig):
#                                     bmethod = m
#                             if not bmethod:
#                                 print(mapped_sig)
#                                 raise Exception("No mapped method found")


#                             new_record = {
#                                 **row,
#                                 "old_file": old_file,
#                                 "new_file": new_file,
#                                 "old_class": aclass["tree_path"],
#                                 "new_class": bclass["tree_path"],
#                                 "old_method_sig": (
#                                     method["name"],
#                                     method["parameters"],
#                                 ),
#                                 "new_method_sig": (
#                                     bmethod["name"],
#                                     method["parameters"],
#                                 ),
#                                 "old_method_code": method["definition"],
#                                 "new_method_code": bmethod["definition"],
#                             }

#                             records.append(new_record)
#     res = pd.DataFrame(records)
#     res.to_csv(args.output, index=False)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument("-d", "--data-file", dest="data_file", help="Input CSV file")
#     parser.add_argument("-s", "--data-storage", dest="data_storage")
#     args = parser.parse_args()
#     main(args)
data_storage = "/drive1/thieulvd/code-generation/"
migration = "ForgeRock_openidm-community-edition__43689602ee8a67deb29ea8412c48410dcaa6b30a__43689602ee8a67deb29ea8412c48410dcaa6b30a"
start_commit = "43689602ee8a67deb29ea8412c48410dcaa6b30a"
end_commit = "43689602ee8a67deb29ea8412c48410dcaa6b30a"
prev_commit = "43689602ee8a67deb29ea8412c48410dcaa6b30a"
repo_name = "ForgeRock_openidm-community-edition"

result = {
    "repo_name": repo_name,
    "start_commit": start_commit,
    "end_commit": end_commit,
    "prev_commit": prev_commit,
    "commits_metadata": {"commit_hash": {"message": "", "author": "", "time": ""}},
    "diff_files": {
        "added": [],
        "deleted": [],
        "modified": [],
        "renamed_unchanged": [],
        "renamed_modified": [],
    },
    "pom_files": {
        "pom_url": [
            {
                "from_lib": {"name": "", "version": ""},
                "to_lib": {"name": "", "version": ""},
            }
        ]
    },
    "java_diff_files": {
        "added": {},
        "deleted": {},
        "modified": {
            "version_1": {},
            "version_2": {
                "openidm-shell/src/main/java/org/forgerock/openidm/shell/felixgogo/Activator.java": [
                    {
                        "version": 2,
                        "ver1_path": "openidm-shell/src/main/java/org/forgerock/openidm/shell/felixgogo/Activator.java",
                        "ver2_path": "openidm-shell/src/main/java/org/forgerock/openidm/shell/felixgogo/Activator.java",
                        "definition": 'public class Activator implements BundleActivator {\n    private static final Logger LOG = Logger.getLogger(Activator.class.getName());\n\n    private static final String COMMANDS_DESCRIPTION_PROPERTY = "openidm.osgi.shell.commands";\n    private static final String GROUP_ID_PROPERTY = "openidm.osgi.shell.group.id";\n\n    /**\n     * Felix GoGo shell API supports groups.\n     * Filter requires shell commands description and group id\n     */\n    private static final String SHELL_COMMANDS_SERVICE_FILTER = "(&" +\n            "(" + COMMANDS_DESCRIPTION_PROPERTY + "=*)" +\n            "(" + GROUP_ID_PROPERTY + "=*)" +\n            ")";\n\n\n    /**\n     * Bundle Context\n     */\n    private BundleContext bc;\n\n    /**\n     * Command provides service tracker\n     */\n    private ServiceTracker shellCommandsTracker;\n\n    private Map<ServiceReference, ServiceRegistration> commandRegistrations = new HashMap<ServiceReference, ServiceRegistration>();\n\n    public void start(BundleContext context) throws Exception {\n        bc = context;\n        shellCommandsTracker = new ServiceTracker(bc, bc.createFilter("(objectClass=" + CustomCommandScope.class.getName() + ")"),\n                new ShellCommandsCustomizer());\n        shellCommandsTracker.open();\n\n        Dictionary<String, Object> props = new Hashtable<String, Object>();\n        props.put(CommandProcessor.COMMAND_SCOPE, "debug");\n        props.put(CommandProcessor.COMMAND_FUNCTION, DebugCommands.functions);\n        bc.registerService(DebugCommands.class.getName(), new DebugCommands(bc), props);\n    }\n\n    public void stop(BundleContext bundleContext) throws Exception {\n        shellCommandsTracker.close();\n        shellCommandsTracker = null;\n\n        bc = null;\n    }\n\n    /**\n     * Validate Command method\n     *\n     * @param service     service instance\n     * @param commandName command method name\n     * @return <code>true</code> if method is peresent in service, <code>public</code> and\n     *         has params <code>PrintStream</code> and <code>String[]</code>, otherwise - <code>false</code>\n     */\n    private boolean isValidCommandMethod(Object service, String commandName) {\n        try {\n            service.getClass().getMethod(commandName, InputStream.class, PrintStream.class, String[].class);\n            return true;\n        } catch (NoSuchMethodException e) {\n            return false;\n        }\n    }\n\n    /**\n     * Command provides service tracker customizer\n     */\n    private class ShellCommandsCustomizer implements ServiceTrackerCustomizer {\n\n        public Object addingService(ServiceReference reference) {\n            CustomCommandScope service = (CustomCommandScope) bc.getService(reference);\n            Object groupId = service.getScope();\n            // if property value null or not String - ignore service\n            if (groupId == null || !(groupId instanceof String)) {\n                LOG.warning(GROUP_ID_PROPERTY + " property is null or invalid. Ignore service");\n                return null;\n            }\n            // get service ranking propety. if not null - use it on Command services registration\n            Map<String, String> commandMap = service.getFunctionMap();\n            if (!commandMap.isEmpty()) {\n                Dictionary<String, Object> props = new Hashtable<String, Object>();\n                Integer ranking = (Integer) reference.getProperty(Constants.SERVICE_RANKING);\n                Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n                if (ranking != null) {\n                    props.put(Constants.SERVICE_RANKING, ranking);\n                }\n                props.put(CommandProcessor.COMMAND_SCOPE, groupId);\n                props.put(CommandProcessor.COMMAND_FUNCTION, commandMap.keySet().toArray(new String[commandMap.size()]));\n                try {\n                    // generate class\n                    Object commandsProvider = FelixGogoCommandsServiceGenerator.generate(service, commandMap, serviceId.toString());\n                    commandRegistrations.put(reference,\n                            bc.registerService(commandsProvider.getClass().getName(), commandsProvider, props));\n                } catch (Exception e) {\n                    LOG.log(Level.WARNING, "Unable to initialize group: " + groupId, e);\n                }\n                return service;\n            } else {\n                return null;\n            }\n        }\n\n        public void modifiedService(ServiceReference reference, Object service) {\n            // ignore\n        }\n\n        public void removedService(ServiceReference reference, Object service) {\n            // unregister CommandGroup services that belongs to this service registration\n            Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n            // detach class\n            FelixGogoCommandsServiceGenerator.clean(serviceId.toString());\n            ServiceRegistration registration = commandRegistrations.remove(reference);\n            if (registration != null) {\n                registration.unregister();\n            }\n            bc.ungetService(reference);\n        }\n    }\n}',
                        "package": "package org.forgerock.openidm.shell.felixgogo;",
                        "tree_path": "Activator",
                        "name": "Activator",
                        "modifiers": "public",
                        "superclass": None,
                        "super_interfaces": "implements BundleActivator",
                        "body": '{\n    private static final Logger LOG = Logger.getLogger(Activator.class.getName());\n\n    private static final String COMMANDS_DESCRIPTION_PROPERTY = "openidm.osgi.shell.commands";\n    private static final String GROUP_ID_PROPERTY = "openidm.osgi.shell.group.id";\n\n    /**\n     * Felix GoGo shell API supports groups.\n     * Filter requires shell commands description and group id\n     */\n    private static final String SHELL_COMMANDS_SERVICE_FILTER = "(&" +\n            "(" + COMMANDS_DESCRIPTION_PROPERTY + "=*)" +\n            "(" + GROUP_ID_PROPERTY + "=*)" +\n            ")";\n\n\n    /**\n     * Bundle Context\n     */\n    private BundleContext bc;\n\n    /**\n     * Command provides service tracker\n     */\n    private ServiceTracker shellCommandsTracker;\n\n    private Map<ServiceReference, ServiceRegistration> commandRegistrations = new HashMap<ServiceReference, ServiceRegistration>();\n\n    public void start(BundleContext context) throws Exception {\n        bc = context;\n        shellCommandsTracker = new ServiceTracker(bc, bc.createFilter("(objectClass=" + CustomCommandScope.class.getName() + ")"),\n                new ShellCommandsCustomizer());\n        shellCommandsTracker.open();\n\n        Dictionary<String, Object> props = new Hashtable<String, Object>();\n        props.put(CommandProcessor.COMMAND_SCOPE, "debug");\n        props.put(CommandProcessor.COMMAND_FUNCTION, DebugCommands.functions);\n        bc.registerService(DebugCommands.class.getName(), new DebugCommands(bc), props);\n    }\n\n    public void stop(BundleContext bundleContext) throws Exception {\n        shellCommandsTracker.close();\n        shellCommandsTracker = null;\n\n        bc = null;\n    }\n\n    /**\n     * Validate Command method\n     *\n     * @param service     service instance\n     * @param commandName command method name\n     * @return <code>true</code> if method is peresent in service, <code>public</code> and\n     *         has params <code>PrintStream</code> and <code>String[]</code>, otherwise - <code>false</code>\n     */\n    private boolean isValidCommandMethod(Object service, String commandName) {\n        try {\n            service.getClass().getMethod(commandName, InputStream.class, PrintStream.class, String[].class);\n            return true;\n        } catch (NoSuchMethodException e) {\n            return false;\n        }\n    }\n\n    /**\n     * Command provides service tracker customizer\n     */\n    private class ShellCommandsCustomizer implements ServiceTrackerCustomizer {\n\n        public Object addingService(ServiceReference reference) {\n            CustomCommandScope service = (CustomCommandScope) bc.getService(reference);\n            Object groupId = service.getScope();\n            // if property value null or not String - ignore service\n            if (groupId == null || !(groupId instanceof String)) {\n                LOG.warning(GROUP_ID_PROPERTY + " property is null or invalid. Ignore service");\n                return null;\n            }\n            // get service ranking propety. if not null - use it on Command services registration\n            Map<String, String> commandMap = service.getFunctionMap();\n            if (!commandMap.isEmpty()) {\n                Dictionary<String, Object> props = new Hashtable<String, Object>();\n                Integer ranking = (Integer) reference.getProperty(Constants.SERVICE_RANKING);\n                Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n                if (ranking != null) {\n                    props.put(Constants.SERVICE_RANKING, ranking);\n                }\n                props.put(CommandProcessor.COMMAND_SCOPE, groupId);\n                props.put(CommandProcessor.COMMAND_FUNCTION, commandMap.keySet().toArray(new String[commandMap.size()]));\n                try {\n                    // generate class\n                    Object commandsProvider = FelixGogoCommandsServiceGenerator.generate(service, commandMap, serviceId.toString());\n                    commandRegistrations.put(reference,\n                            bc.registerService(commandsProvider.getClass().getName(), commandsProvider, props));\n                } catch (Exception e) {\n                    LOG.log(Level.WARNING, "Unable to initialize group: " + groupId, e);\n                }\n                return service;\n            } else {\n                return null;\n            }\n        }\n\n        public void modifiedService(ServiceReference reference, Object service) {\n            // ignore\n        }\n\n        public void removedService(ServiceReference reference, Object service) {\n            // unregister CommandGroup services that belongs to this service registration\n            Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n            // detach class\n            FelixGogoCommandsServiceGenerator.clean(serviceId.toString());\n            ServiceRegistration registration = commandRegistrations.remove(reference);\n            if (registration != null) {\n                registration.unregister();\n            }\n            bc.ungetService(reference);\n        }\n    }\n}',
                        "start_point": {"row": 48, "column": 0},
                        "end_point": {"row": 166, "column": 1},
                        "file_mode": "Modified",
                        "methods": [
                            {
                                "definition": 'public void start(BundleContext context) throws Exception {\n    bc = context;\n    shellCommandsTracker = new ServiceTracker(bc, bc.createFilter("(objectClass=" + CustomCommandScope.class.getName() + ")"),\n            new ShellCommandsCustomizer());\n    shellCommandsTracker.open();\n\n    Dictionary<String, Object> props = new Hashtable<String, Object>();\n    props.put(CommandProcessor.COMMAND_SCOPE, "debug");\n    props.put(CommandProcessor.COMMAND_FUNCTION, DebugCommands.functions);\n    bc.registerService(DebugCommands.class.getName(), new DebugCommands(bc), props);\n}',
                                "name": "start",
                                "modifiers": "public",
                                "return_type": None,
                                "parameters": [
                                    {"type": "BundleContext", "name": "context"}
                                ],
                                "body": '{\n    bc = context;\n    shellCommandsTracker = new ServiceTracker(bc, bc.createFilter("(objectClass=" + CustomCommandScope.class.getName() + ")"),\n            new ShellCommandsCustomizer());\n    shellCommandsTracker.open();\n\n    Dictionary<String, Object> props = new Hashtable<String, Object>();\n    props.put(CommandProcessor.COMMAND_SCOPE, "debug");\n    props.put(CommandProcessor.COMMAND_FUNCTION, DebugCommands.functions);\n    bc.registerService(DebugCommands.class.getName(), new DebugCommands(bc), props);\n}',
                                "start_point": {"row": 76, "column": 4},
                                "end_point": {"row": 86, "column": 5},
                                "ver2_signature": "start__BundleContext",
                                "method_mode": "Modified",
                                "ver1_signature": "start__BundleContext",
                            },
                            {
                                "definition": "public void stop(BundleContext bundleContext) throws Exception {\n    shellCommandsTracker.close();\n    shellCommandsTracker = null;\n\n    bc = null;\n}",
                                "name": "stop",
                                "modifiers": "public",
                                "return_type": None,
                                "parameters": [
                                    {"type": "BundleContext", "name": "bundleContext"}
                                ],
                                "body": "{\n    shellCommandsTracker.close();\n    shellCommandsTracker = null;\n\n    bc = null;\n}",
                                "start_point": {"row": 88, "column": 4},
                                "end_point": {"row": 93, "column": 5},
                                "ver2_signature": "stop__BundleContext",
                                "method_mode": "Unchanged",
                                "ver1_signature": "stop__BundleContext",
                            },
                            {
                                "definition": "private boolean isValidCommandMethod(Object service, String commandName) {\n    try {\n        service.getClass().getMethod(commandName, InputStream.class, PrintStream.class, String[].class);\n        return true;\n    } catch (NoSuchMethodException e) {\n        return false;\n    }\n}",
                                "name": "isValidCommandMethod",
                                "modifiers": "private",
                                "return_type": None,
                                "parameters": [
                                    {"type": "Object", "name": "service"},
                                    {"type": "String", "name": "commandName"},
                                ],
                                "body": "{\n    try {\n        service.getClass().getMethod(commandName, InputStream.class, PrintStream.class, String[].class);\n        return true;\n    } catch (NoSuchMethodException e) {\n        return false;\n    }\n}",
                                "start_point": {"row": 103, "column": 4},
                                "end_point": {"row": 110, "column": 5},
                                "ver2_signature": "isValidCommandMethod__Object__String",
                                "method_mode": "Unchanged",
                                "ver1_signature": "isValidCommandMethod__Object__String",
                            },
                        ],
                        "class_mode": "Modified",
                        "ver1_tree_path": "Activator",
                        "ver2_tree_path": "Activator",
                    },
                    {
                        "version": 2,
                        "ver1_path": "openidm-shell/src/main/java/org/forgerock/openidm/shell/felixgogo/Activator.java",
                        "ver2_path": "openidm-shell/src/main/java/org/forgerock/openidm/shell/felixgogo/Activator.java",
                        "definition": 'private class ShellCommandsCustomizer implements ServiceTrackerCustomizer {\n\n    public Object addingService(ServiceReference reference) {\n        CustomCommandScope service = (CustomCommandScope) bc.getService(reference);\n        Object groupId = service.getScope();\n        // if property value null or not String - ignore service\n        if (groupId == null || !(groupId instanceof String)) {\n            LOG.warning(GROUP_ID_PROPERTY + " property is null or invalid. Ignore service");\n            return null;\n        }\n        // get service ranking propety. if not null - use it on Command services registration\n        Map<String, String> commandMap = service.getFunctionMap();\n        if (!commandMap.isEmpty()) {\n            Dictionary<String, Object> props = new Hashtable<String, Object>();\n            Integer ranking = (Integer) reference.getProperty(Constants.SERVICE_RANKING);\n            Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n            if (ranking != null) {\n                props.put(Constants.SERVICE_RANKING, ranking);\n            }\n            props.put(CommandProcessor.COMMAND_SCOPE, groupId);\n            props.put(CommandProcessor.COMMAND_FUNCTION, commandMap.keySet().toArray(new String[commandMap.size()]));\n            try {\n                // generate class\n                Object commandsProvider = FelixGogoCommandsServiceGenerator.generate(service, commandMap, serviceId.toString());\n                commandRegistrations.put(reference,\n                        bc.registerService(commandsProvider.getClass().getName(), commandsProvider, props));\n            } catch (Exception e) {\n                LOG.log(Level.WARNING, "Unable to initialize group: " + groupId, e);\n            }\n            return service;\n        } else {\n            return null;\n        }\n    }\n\n    public void modifiedService(ServiceReference reference, Object service) {\n        // ignore\n    }\n\n    public void removedService(ServiceReference reference, Object service) {\n        // unregister CommandGroup services that belongs to this service registration\n        Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n        // detach class\n        FelixGogoCommandsServiceGenerator.clean(serviceId.toString());\n        ServiceRegistration registration = commandRegistrations.remove(reference);\n        if (registration != null) {\n            registration.unregister();\n        }\n        bc.ungetService(reference);\n    }\n}',
                        "package": "package org.forgerock.openidm.shell.felixgogo;",
                        "tree_path": "Activator.ShellCommandsCustomizer",
                        "name": "ShellCommandsCustomizer",
                        "modifiers": "private",
                        "superclass": None,
                        "super_interfaces": "implements ServiceTrackerCustomizer",
                        "body": '{\n\n    public Object addingService(ServiceReference reference) {\n        CustomCommandScope service = (CustomCommandScope) bc.getService(reference);\n        Object groupId = service.getScope();\n        // if property value null or not String - ignore service\n        if (groupId == null || !(groupId instanceof String)) {\n            LOG.warning(GROUP_ID_PROPERTY + " property is null or invalid. Ignore service");\n            return null;\n        }\n        // get service ranking propety. if not null - use it on Command services registration\n        Map<String, String> commandMap = service.getFunctionMap();\n        if (!commandMap.isEmpty()) {\n            Dictionary<String, Object> props = new Hashtable<String, Object>();\n            Integer ranking = (Integer) reference.getProperty(Constants.SERVICE_RANKING);\n            Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n            if (ranking != null) {\n                props.put(Constants.SERVICE_RANKING, ranking);\n            }\n            props.put(CommandProcessor.COMMAND_SCOPE, groupId);\n            props.put(CommandProcessor.COMMAND_FUNCTION, commandMap.keySet().toArray(new String[commandMap.size()]));\n            try {\n                // generate class\n                Object commandsProvider = FelixGogoCommandsServiceGenerator.generate(service, commandMap, serviceId.toString());\n                commandRegistrations.put(reference,\n                        bc.registerService(commandsProvider.getClass().getName(), commandsProvider, props));\n            } catch (Exception e) {\n                LOG.log(Level.WARNING, "Unable to initialize group: " + groupId, e);\n            }\n            return service;\n        } else {\n            return null;\n        }\n    }\n\n    public void modifiedService(ServiceReference reference, Object service) {\n        // ignore\n    }\n\n    public void removedService(ServiceReference reference, Object service) {\n        // unregister CommandGroup services that belongs to this service registration\n        Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n        // detach class\n        FelixGogoCommandsServiceGenerator.clean(serviceId.toString());\n        ServiceRegistration registration = commandRegistrations.remove(reference);\n        if (registration != null) {\n            registration.unregister();\n        }\n        bc.ungetService(reference);\n    }\n}',
                        "start_point": {"row": 115, "column": 4},
                        "end_point": {"row": 165, "column": 5},
                        "file_mode": "Modified",
                        "methods": [
                            {
                                "definition": 'public Object addingService(ServiceReference reference) {\n    CustomCommandScope service = (CustomCommandScope) bc.getService(reference);\n    Object groupId = service.getScope();\n    // if property value null or not String - ignore service\n    if (groupId == null || !(groupId instanceof String)) {\n        LOG.warning(GROUP_ID_PROPERTY + " property is null or invalid. Ignore service");\n        return null;\n    }\n    // get service ranking propety. if not null - use it on Command services registration\n    Map<String, String> commandMap = service.getFunctionMap();\n    if (!commandMap.isEmpty()) {\n        Dictionary<String, Object> props = new Hashtable<String, Object>();\n        Integer ranking = (Integer) reference.getProperty(Constants.SERVICE_RANKING);\n        Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n        if (ranking != null) {\n            props.put(Constants.SERVICE_RANKING, ranking);\n        }\n        props.put(CommandProcessor.COMMAND_SCOPE, groupId);\n        props.put(CommandProcessor.COMMAND_FUNCTION, commandMap.keySet().toArray(new String[commandMap.size()]));\n        try {\n            // generate class\n            Object commandsProvider = FelixGogoCommandsServiceGenerator.generate(service, commandMap, serviceId.toString());\n            commandRegistrations.put(reference,\n                    bc.registerService(commandsProvider.getClass().getName(), commandsProvider, props));\n        } catch (Exception e) {\n            LOG.log(Level.WARNING, "Unable to initialize group: " + groupId, e);\n        }\n        return service;\n    } else {\n        return null;\n    }\n}',
                                "name": "addingService",
                                "modifiers": "public",
                                "return_type": "Object",
                                "parameters": [
                                    {"type": "ServiceReference", "name": "reference"}
                                ],
                                "body": '{\n    CustomCommandScope service = (CustomCommandScope) bc.getService(reference);\n    Object groupId = service.getScope();\n    // if property value null or not String - ignore service\n    if (groupId == null || !(groupId instanceof String)) {\n        LOG.warning(GROUP_ID_PROPERTY + " property is null or invalid. Ignore service");\n        return null;\n    }\n    // get service ranking propety. if not null - use it on Command services registration\n    Map<String, String> commandMap = service.getFunctionMap();\n    if (!commandMap.isEmpty()) {\n        Dictionary<String, Object> props = new Hashtable<String, Object>();\n        Integer ranking = (Integer) reference.getProperty(Constants.SERVICE_RANKING);\n        Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n        if (ranking != null) {\n            props.put(Constants.SERVICE_RANKING, ranking);\n        }\n        props.put(CommandProcessor.COMMAND_SCOPE, groupId);\n        props.put(CommandProcessor.COMMAND_FUNCTION, commandMap.keySet().toArray(new String[commandMap.size()]));\n        try {\n            // generate class\n            Object commandsProvider = FelixGogoCommandsServiceGenerator.generate(service, commandMap, serviceId.toString());\n            commandRegistrations.put(reference,\n                    bc.registerService(commandsProvider.getClass().getName(), commandsProvider, props));\n        } catch (Exception e) {\n            LOG.log(Level.WARNING, "Unable to initialize group: " + groupId, e);\n        }\n        return service;\n    } else {\n        return null;\n    }\n}',
                                "start_point": {"row": 117, "column": 8},
                                "end_point": {"row": 148, "column": 9},
                                "ver2_signature": "addingService__ServiceReference",
                                "method_mode": "Modified",
                                "ver1_signature": "addingService__ServiceReference",
                            },
                            {
                                "definition": "public void modifiedService(ServiceReference reference, Object service) {\n    // ignore\n}",
                                "name": "modifiedService",
                                "modifiers": "public",
                                "return_type": None,
                                "parameters": [
                                    {"type": "ServiceReference", "name": "reference"},
                                    {"type": "Object", "name": "service"},
                                ],
                                "body": "{\n    // ignore\n}",
                                "start_point": {"row": 150, "column": 8},
                                "end_point": {"row": 152, "column": 9},
                                "ver2_signature": "modifiedService__ServiceReference__Object",
                                "method_mode": "Unchanged",
                                "ver1_signature": "modifiedService__ServiceReference__Object",
                            },
                            {
                                "definition": "public void removedService(ServiceReference reference, Object service) {\n    // unregister CommandGroup services that belongs to this service registration\n    Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n    // detach class\n    FelixGogoCommandsServiceGenerator.clean(serviceId.toString());\n    ServiceRegistration registration = commandRegistrations.remove(reference);\n    if (registration != null) {\n        registration.unregister();\n    }\n    bc.ungetService(reference);\n}",
                                "name": "removedService",
                                "modifiers": "public",
                                "return_type": None,
                                "parameters": [
                                    {"type": "ServiceReference", "name": "reference"},
                                    {"type": "Object", "name": "service"},
                                ],
                                "body": "{\n    // unregister CommandGroup services that belongs to this service registration\n    Long serviceId = (Long) reference.getProperty(Constants.SERVICE_ID);\n    // detach class\n    FelixGogoCommandsServiceGenerator.clean(serviceId.toString());\n    ServiceRegistration registration = commandRegistrations.remove(reference);\n    if (registration != null) {\n        registration.unregister();\n    }\n    bc.ungetService(reference);\n}",
                                "start_point": {"row": 154, "column": 8},
                                "end_point": {"row": 164, "column": 9},
                                "ver2_signature": "removedService__ServiceReference__Object",
                                "method_mode": "Unchanged",
                                "ver1_signature": "removedService__ServiceReference__Object",
                            },
                        ],
                        "class_mode": "Modified",
                        "ver1_tree_path": "Activator.ShellCommandsCustomizer",
                        "ver2_tree_path": "Activator.ShellCommandsCustomizer",
                    },
                ]
            },
        },
        "renamed_modified": {},
        "renamed_unchanged": {},
    },
}

import pandas as pd

df = pd.read_csv("data/migrations_36_file.csv")

x = dict(df[df["id"] == migration].iloc[0])

for file in eval(x["added"]):
    if file.endswith(".java") or file.endswith("pom.xml"):
        continue
    result["diff_files"]["added"].append(file)

for file in eval(x["deleted"]):
    if file.endswith(".java") or file.endswith("pom.xml"):
        continue
    result["diff_files"]["deleted"].append(file)

for file in eval(x["modified"]):
    if file.endswith(".java") or file.endswith("pom.xml"):
        continue
    result["diff_files"]["modified"].append(file)

for file in eval(x["renamed_unchanged"]):
    print(file)
    old, new = file.values()
    if (
        old.endswith(".java")
        or new.endswith(".java")
        or old.endswith("pom.xml")
        or old.endswith("pom.xml")
    ):
        continue
    result["diff_files"]["renamed_unchanged"].append(file)

for file in eval(x["renamed_modified"]):
    old, new, _ = file.values()
    if (
        old.endswith(".java")
        or new.endswith(".java")
        or old.endswith("pom.xml")
        or old.endswith("pom.xml")
    ):
        continue
    result["diff_files"]["renamed_unchanged"].append(file)


# for file in eval(x["java_added"]):
#     result["java_diff_files"]["added"].append()

# for file in eval(x["deleted"]):
#     if file.endswith(".java") or file.endswith("pom.xml"):
#         continue
#     result["diff_files"]["deleted"].append(file)

# for file in eval(x["modified"]):
#     if file.endswith(".java") or file.endswith("pom.xml"):
#         continue
#     result["diff_files"]["modified"].append(file)

# for file in eval(x["renamed_unchanged"]):
#     print(file)
#     old, new = file.values()
#     if old.endswith(".java") or new.endswith(".java") or old.endswith("pom.xml") or old.endswith("pom.xml"):
#         continue
#     result["diff_files"]["renamed_unchanged"].append(file)

# for file in eval(x["renamed_unchanged"]):
#     old, new, _ = file.values()
#     if old.endswith(".java") or new.endswith(".java") or old.endswith("pom.xml") or old.endswith("pom.xml"):
#         continue
#     result["diff_files"]["renamed_unchanged"].append(file)
print(json.dumps(result, indent=4))
