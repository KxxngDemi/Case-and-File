create:
	touch to_do.db
	rm to_do.db
	python3 create_new_db.py
	python3 home_page.py
	python3 task_notification.py
	
start:
	python3 home_page.py
	python3 task_notification.py

run:
	python3 to_do_list.py
	python3 task_notification.py

test:
	python3 -m unittest test_home_page.py
	python3 -m unittest test_create_new_db.py
	python3 -m unittest test_task_notification.py

clear:
	rm -rf __pycache__
