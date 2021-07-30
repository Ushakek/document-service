class EditorHTML:
    """ Класс для создания / заполнения HTML документа

    Реализованы методы:
        - Заполняет строку таблицы значениями;
        - Заполняет строку таблицы значениями с объединением последующих N столбцов;
        - Заполняет строку таблицы значениями с объединением последующих N строк;
    """

    @staticmethod
    def fill_columns(values: list = None):
        """ Заполняет строку таблицы значениями из аргумента

        Args:
            values (optional, list): Список значений для заполнения строки таблицы
        Returns:
            Строка заполненного html шаблона для одной строки таблицы
        Examples:

        >>> EditorHTML.fill_columns(['Value1', None, 'Value3']) #doctest:+ELLIPSIS
        '\\n        <tr>\\n        <td>Value1</td><td>―</td><td>Value3</td>\\n        </tr>\\n        '
        >>> # This is equal for HTML_table => \
        |Value1| - |Value3|

        >>> EditorHTML.fill_columns()
        '\\n        <tr>\\n        <td>―</td>\\n        </tr>\\n        '
        >>> # This is equal for HTML_table => \
        | - |
        """
        html_row = """
        <tr>
        {data_columns}
        </tr>
        """
        if not values:
            values = [None]

        columns = ''
        for value in values:
            if value is None:
                value = '―'
            columns += f'<td>{value}</td>'

        return html_row.format(data_columns=columns)

    @staticmethod
    def fill_merged_column(values: list = None, column_number: int = 0):
        """ Заполняет строку таблицы значениями, объединяя последнюю колонку с N кол-вом столбцов

        Args:
            values (optional, list): Список значений для заполнения строки таблицы
            column_number (optional, int): Кол-во столбцов в таблице
        Returns:
            Строка заполненного html шаблона для одной строки таблицы
        Examples:

        >>> EditorHTML.fill_merged_column(['Value1', None, 'Value3'], 5)
        '\\n        <tr>\\n        <td>Value1</td><td>―</td><td colspan="3">Value3</td>\\n        </tr>\\n        '
        >>> # This is equal for HTML_table => \
        | PreviousValue1 | PreviousValue2 | PreviousValue3 | PreviousValue4 | PreviousValue5 | \
        | Value1         |         -      | Value3                                           |
        """
        html_row = """
        <tr>
        {data_columns}
        </tr>
        """
        if not values:
            values = [None]

        columns = ''
        for index, value in enumerate(values):
            if value is None:
                value = '―'
            # В последнюю колонку объединяет с оставшимся кол-вом
            if index == len(values)-1:
                columns += f'<td colspan="{column_number-index}">' \
                           f'{value}' \
                           f'</td>'
            else:
                columns += f'<td>{value}</td>'
        return html_row.format(data_columns=columns)

    @staticmethod
    def fill_merged_row(values: list = None, row_number: int = 0):
        """ Заполняет строку таблицы заполняя столбцы и объединяя N последующих строк в таблице

        Args:
            values (optional, list): Список значений для заполнения строки таблицы
            row_number(optional, int): Кол-во последующих строк, которые будут объединены
        Returns:
            Строка заполненного html шаблона для одной строки таблицы
        Examples:

        >>> EditorHTML.fill_merged_row(['Value1', None, 'Value3'], 3)
        '\\n        <tr>\\n        <td rowspan="4">Value1</td><td rowspan="4">―</td><td rowspan="4">Value3</td>\\n        </tr>\\n        '
        >>> # This is equal for HTML_table => \
        |        |   |        | NextRow1 | \
        | Value1 | - | Value3 | NextRow2 | \
        |        |   |        | NextRow3 |
        """
        html_row = """
        <tr>
        {data_columns}
        </tr>
        """
        if not values:
            values = [None]

        columns = ''
        for value in values:
            if value is None:
                value = '―'

            columns += f'<td rowspan="{row_number+1}">{value}</td>'

        return html_row.format(data_columns=columns)

