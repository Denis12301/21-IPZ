... from graphviz import Digraph
... diagram = Digraph('UC1_Client_Management', format='png')
... diagram.attr(rankdir='LR', size='8,5')
... diagram.attr('node', shape='box', style='filled', color='lightblue')
... 
... diagram.node('Start', 'Початок')
... diagram.node('Input', 'Введення/вибір дії (додати/переглянути/редагувати/видалити)')
... diagram.node('Add', 'Додавання нового клієнта')
... diagram.node('View', 'Перегляд інформації про клієнта')
... diagram.node('Edit', 'Редагування даних клієнта')
... diagram.node('Delete', 'Видалення клієнта')
... diagram.node('End', 'Кінець')
... 
... diagram.edge('Start', 'Input')
... diagram.edge('Input', 'Add', label='якщо "додати"')
... diagram.edge('Input', 'View', label='якщо "переглянути"')
... diagram.edge('Input', 'Edit', label='якщо "редагувати"')
... diagram.edge('Input', 'Delete', label='якщо "видалити"')
... 
... diagram.edge('Add', 'Input')
... diagram.edge('View', 'Input')
... diagram.edge('Edit', 'Input')
... diagram.edge('Delete', 'Input')
... 
... diagram.edge('Input', 'End', label='вийти')
... 
... diagram.render('uc1_client_flow', cleanup=True)
... print("[OK] Діаграма збережена як uc1_client_flow.png")
