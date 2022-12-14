# The Threads project. Be an expert.

В этом сервисе вы можете задать вопрос и получить на него ответ.

### Вы можете применить это двумя способами:

1 - Если вы оказываете образовательные услуги, вы можете сформировать сообщество студентов, которые будут самостоятельно задавать и отвечать на возникшие во время обучения вопросы. Это позволит вам снизить нагрузку на менторов и преподавателей, а так же повысить качество обучения, ведь нет ничего лучше для усвоения материала, чем объяснить что то другому человеку.

Кроме того, сформированное вами сообщество выпускников и текущих студентов, позволит вам переиспользовать имеющиеся знания и материал и улучшить кооперацию студентов, а так же повысить престиж вашего образовательного проекта, если захотите сделать площадку публичной, где ваши менторы и студенты смогут сделать вклад в сообщество. В любом случае, вы полностью управляете инфраструктурой и данными, ведь вы можете развернуть собственный инстанс.

2 - Если у вас значительное число разработчиков, работающих распределенно и вы хотите сохранить институцианальные знания внутри компании, вы можете развернуть этот сервис в вашей внутренней инраструктуре и предоставить доступ только вашим сотрудникам и в этом случае вы получите единую платформу для сохранения знаний, защищающую вас от внешнего контура, а так же от изменениях в команде.

### Запуск:

Склонируйте репозиторий:
<pre><code>git clone https://github.com/yagunov-test-moscow/the-threads-project.git</code></pre>

Создайте виртуально окружение:
<pre><code>python3 -m venv venv</code></pre>

Активируйте его:
<pre><code>source venv/bin/activate</code></pre>

Обновите pip:
<pre><code>python3 -m pip install --upgrade pip</code></pre>

Установите все зависимости:
<pre><code>pip install -r requirements.txt</code></pre>

Запустите сервер:
<pre><code>python manage.py runserver</code></pre>
