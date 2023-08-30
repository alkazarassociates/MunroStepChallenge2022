/usr/lib/postgresql/11/bin/pg_dump -d tsc23 --clean --create | /usr/lib/postgresql/11/bin/psql -h test.alkazarassociates.com -U django
/usr/lib/postgresql/11/bin/psql -h test.alkazarassociates.com -U django -c "DROP DATABASE django_test"
/usr/lib/postgresql/11/bin/psql -h test.alkazarassociates.com -U django -c "CREATE DATABASE django_test WITH TEMPLATE tsc23 OWNER django"
