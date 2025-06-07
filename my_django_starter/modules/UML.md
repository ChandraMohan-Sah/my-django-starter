+----------------------+
|      OSDetector      |
+----------------------+
| + execute(context)   |
+----------------------+
<<implements Step>>

+--------------------------+
|    VirtualEnvCreator     |
+--------------------------+
| + execute(context)       |
+--------------------------+
<<implements Step>>


+-----------------------+
|    DjangoInstaller    |
+-----------------------+
| + execute(context)    |
+-----------------------+
<<implements Step>>


+-----------------------+
|    ProjectCreator     |
+-----------------------+
| + execute(context)    |
+-----------------------+
<<implements Step>>


+-----------------------+
|      AppCreator       |
+-----------------------+
| + execute(context)    |
+-----------------------+
<<implements Step>>


+-----------------------+
|   SettingsModifier    |
+-----------------------+
| + execute(context)    |
+-----------------------+
<<implements Step>>



+-----------------------+
| RequirementsGenerator |
+-----------------------+
| + execute(context)    |
+-----------------------+
<<implements Step>>