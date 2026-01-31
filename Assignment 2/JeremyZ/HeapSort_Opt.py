import pandas as pd


def heapify(arr, parent, asc):
    left_child = parent * 2 + 1
    right_child = parent * 2 + 2

    if left_child < arr.shape[0]:

        if asc == False:
            if right_child < arr.shape[0] and arr[left_child, 1] == max(arr[parent, 1],
                                                                                  arr[left_child, 1],
                                                                                  arr[right_child, 1]):
                arr[[parent, left_child], :] = arr[[left_child, parent], :]
                heapify(arr, left_child, asc)

            if right_child < arr.shape[0] and arr[right_child, 1] == max(arr[parent, 1],
                                                                                   arr[right_child, 1],
                                                                                   arr[left_child, 1]):
                arr[[parent, right_child], :] = arr[[right_child, parent], :]
                heapify(arr, right_child, asc)

            if right_child == arr.shape[0] and arr[left_child, 1] > arr[parent, 1]:
                arr[[parent, left_child], :] = arr[[left_child, parent], :]

        elif asc == True:
            if right_child < arr.shape[0] and arr[left_child, 1] == min(arr[parent, 1],
                                                                                  arr[right_child, 1],
                                                                                  arr[left_child, 1]):
                arr[[parent, left_child], :] = arr[[left_child, parent], :]
                heapify(arr, left_child, asc)

            if right_child < arr.shape[0] and arr[right_child, 1] == min(arr[parent, 1],
                                                                                   arr[right_child, 1],
                                                                                   arr[left_child, 1]):
                arr[[parent, right_child], :] = arr[[right_child, parent], :]
                heapify(arr, right_child, asc)

            if right_child == arr.shape[0] and arr[left_child, 1] < arr[parent, 1]:
                arr[[parent, left_child], :] = arr[[left_child, parent], :]


def sort(df, target, asc):
    sorted_df = pd.DataFrame(columns=df.columns).astype(df.dtypes.to_dict())
    arr = df[target].reset_index(drop=False).to_numpy()

    while arr.shape[0] > 1:
        for parent in range((arr.shape[0] // 2 - 1), -1, -1):
            heapify(arr, parent, asc)
        sorted_df = pd.concat([sorted_df, df.loc[[arr[0,0]], :]], ignore_index=True)
        arr = arr[1:, :]
    else:
        sorted_df = pd.concat([sorted_df, df.loc[[arr[0,0]], :]], ignore_index=True)

    return sorted_df
