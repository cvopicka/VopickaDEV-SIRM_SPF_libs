def classify(
    classes: dict[str, dict[int, dict[str, int | float]]] | None,
    id: str,
    value: int | float,
) -> int | None:
    """Classify values based on FPS CLASSES Table

    Args:
        classes (dict[str, dict[int, dict[str, int | float]]]): All FPS CLASSES Table classes
        id (str): Class of interest
        value (int | float): Value to classify

    Returns:
        int: Class if successful else None
    """
    if not classes:
        return None

    if id not in classes.keys():
        return None

    myclass = classes[id]

    for classid, classvals in myclass.items():
        # Not possible
        if classvals["LT"] == classvals["EQ"] == classvals["GT"]:
            continue

        # Less than equal to
        if classvals["LT"] == classvals["EQ"] and classvals["GT"] is None:
            if value <= classvals["EQ"]:
                return classid

        # Greater than equal to
        if classvals["GT"] == classvals["EQ"] and classvals["LT"] is None:
            if value >= classvals["EQ"]:
                return classid

        # Greater than
        if (
            classvals["LT"] is None
            and classvals["EQ"] is None
            and classvals["GT"] is not None
        ):
            if value > classvals["GT"]:
                return classid

        # Less than
        if (
            classvals["LT"] is not None
            and classvals["EQ"] is None
            and classvals["GT"] is None
        ):
            if value < classvals["LT"]:
                return classid

        # Equal to
        if (
            classvals["LT"] is None
            and classvals["EQ"] is not None
            and classvals["GT"] is None
        ):
            if value == classvals["EQ"]:
                return classid

        # Between with includes
        if (
            classvals["LT"] is not None
            and classvals["EQ"] is not None
            and classvals["GT"] is not None
        ) and classvals["LT"] >= classvals["GT"]:
            # Less than equal to and greater than
            if classvals["LT"] == classvals["EQ"]:
                if value <= classvals["LT"] and value > classvals["GT"]:
                    return classid
            # Greater than equal to and less than
            elif classvals["GT"] == classvals["EQ"]:
                if value >= classvals["GT"] and value < classvals["LT"]:
                    return classid
            # Malformed between
            else:
                continue

        # Between NOT inclusive or Not between
        if (
            classvals["LT"] is not None
            and classvals["EQ"] is None
            and classvals["GT"] is not None
        ):
            if value < classvals["LT"] and value > classvals["GT"]:
                return classid

    return None
