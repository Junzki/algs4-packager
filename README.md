# algs4-packager
A packager for Princeton's Algorithm on Coursera.


## Requirements
- Python 3.6+
- Works under Linux, macOS and Windows.


## Basic Usage
1. Copy and rename `package.sample.json` to `package.json` and put it into your source code directory.
2. Edit the newly created `package.json`, change the file names in field `required_files` to those you actually 
   want to submit.
3. Execute command below.
    ```
    python package.py  /path/to/source/code/directory
    ```
4. Now you can find a newly created zip package like `<ProjectName.zip>` in your working directory.
5. Submit the `<ProjectName.zip>`

### Example
1. When you are about to submit the `Precolation` task, directory tree like below:
    ```
    .
    ├──src
    |  └── main
    |      └── java
    |          └── Percolation
    |              ├── Percolation.java
    |              └── PercolationStats.java
    └── package.py
    ```

2. Copy `package.sample.json`, edit, rename it to `package.json` and add it to `Percolation` directory, like below:
    ```
    .
    ├──src
    |  └── main
    |      └── java
    |          └── Percolation
    |              ├── Percolation.java
    |              ├── PercolationStats.java
    |              └── package.json
    └── package.py
    ```

    Content in `package.json` like below:
    ```json
    {
    "required_files": [
        "Percolation.java",
        "PercolationStats.java"
    ],
    "remove_package_statement": true
    }
    ```

3. Now, run `package.py`
    ```
    python3 package.py src/main/java/Percolation
    ```
    __⚠️ Note: Do NOT use Python 2.x__

4. After execution, you can see a newly created `Percolation.zip` in current directory, like below:
    ```
    .
    ├── src
    |   └── main
    |       └── java
    |           └── Percolation
    |               ├── Percolation.java
    |               ├── PercolationStats.java
    |               └── package.json
    ├── package.py
    └── Percolation.zip
    ```

5. Submit the `Percolation.zip`, and wait for grader feedback.


Hope this small script can do some help :)

## License
BSD 3-Clause License
