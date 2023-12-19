import time
from ..driver import generate_driver, find_element_by_selector
import logging
import random

logger = logging.getLogger("webscrapping")

# Udemy does not load categories menu for webscrapping
# 0 => URL, 1 => TOPIC PT-BR, 2 => TOPIC EN
UDEMY_TOPICS = [
    ["https://www.udemy.com/topic/javascript/", "JavaScript", "JavaScript"],
    ["https://www.udemy.com/topic/react/", "React JS", "React JS"],
    ["https://www.udemy.com/topic/angular/", "Angular", "Angular"],
    ["https://www.udemy.com/topic/css/", "CSS", "CSS"],
    ["https://www.udemy.com/topic/nodejs/", "Node.Js", "Node.Js"],
    ["https://www.udemy.com/topic/aspnet-core/", "ASP.NET Core", "ASP.NET Core"],
    ["https://www.udemy.com/topic/typescript/", "TypeScript", "TypeScript"],
    ["https://www.udemy.com/topic/nextjs-p/", "Next.js", "Next.js"],
    ["https://www.udemy.com/topic/python/", "Python", "Python"],
    [
        "https://www.udemy.com/topic/machine-learning/",
        "Machine Learning",
        "Machine Learning",
    ],
    [
        "https://www.udemy.com/topic/deep-learning/",
        "Aprendizado profundo",
        "Deep Learning",
    ],
    [
        "https://www.udemy.com/topic/artificial-intelligence/",
        "Inteligência artificial",
        "Artificial Intelligence",
    ],
    ["https://www.udemy.com/topic/langchain/", "LangChain", "LangChain"],
    [
        "https://www.udemy.com/topic/natural-language-processing/",
        "Processamento de linguagem natural",
        "Natural Language Processing",
    ],
    [
        "https://www.udemy.com/topic/r-programming-language/",
        "R (linguagem de programação)",
        "R (Programming Language)",
    ],
    ["https://www.udemy.com/topic/tensorflow/", "TensorFlow", "TensorFlow"],
    ["https://www.udemy.com/topic/google-flutter/", "Google Flutter", "Google Flutter"],
    [
        "https://www.udemy.com/topic/ios-development/",
        "Desenvolvimento em iOS",
        "iOS Development",
    ],
    [
        "https://www.udemy.com/topic/android-development/",
        "Desenvolvimento para Android",
        "Android Development",
    ],
    ["https://www.udemy.com/topic/react-native/", "React Native", "React Native"],
    [
        "https://www.udemy.com/topic/dart-programming-language/",
        "Dart (linguagem de programação)",
        "Dart (Programming Language)",
    ],
    ["https://www.udemy.com/topic/swift/", "Swift", "Swift"],
    ["https://www.udemy.com/topic/swiftui/", "SwiftUI", "SwiftUI"],
    ["https://www.udemy.com/topic/kotlin/", "Kotlin", "Kotlin"],
    [
        "https://www.udemy.com/topic/app-development/",
        "Desenvolvimento de aplicativos",
        "App Development",
    ],
    ["https://www.udemy.com/topic/java/", "Java", "Java"],
    [
        "https://www.udemy.com/topic/c-sharp/",
        "C# (linguagem de programação)",
        "C# (Programming Language)",
    ],
    [
        "https://www.udemy.com/topic/c-plus-plus/",
        "C++ (linguagem de programação)",
        "C++ (Programming Language)",
    ],
    [
        "https://www.udemy.com/topic/go-programming-language/",
        "Go (linguagem de programação)",
        "Go (Programming Language)",
    ],
    [
        "https://www.udemy.com/topic/spring-framework/",
        "Spring Framework",
        "Spring Framework",
    ],
    ["https://www.udemy.com/topic/unreal-engine/", "Unreal Engine", "Unreal Engine"],
    ["https://www.udemy.com/topic/unity/", "Unity", "Unity"],
    [
        "https://www.udemy.com/topic/game-development/",
        "Fundamentos do desenvolvimento de games",
        "Fundamentals of Game Development",
    ],
    [
        "https://www.udemy.com/topic/c-plus-plus/",
        "C++ (linguagem de programação)",
        "C++ (Programming Language)",
    ],
    [
        "https://www.udemy.com/topic/c-sharp/",
        "C# (linguagem de programação)",
        "C# (Programming Language)",
    ],
    ["https://www.udemy.com/topic/godot/", "Godot", "Godot"],
    [
        "https://www.udemy.com/topic/3d-game-development/",
        "Desenvolvimento de games 3D",
        "3D Game Development",
    ],
    [
        "https://www.udemy.com/topic/2d-game-development/",
        "Desenvolvimento de games 2D",
        "2D Game Development",
    ],
    [
        "https://www.udemy.com/topic/unreal-engine-blueprints/",
        "Blueprints da Unreal Engine",
        "Unreal Engine Blueprints",
    ],
    ["https://www.udemy.com/topic/sql/", "SQL", "SQL"],
    ["https://www.udemy.com/topic/mysql/", "MySQL", "MySQL"],
    [
        "https://www.udemy.com/topic/database-management/",
        "Database Management Systems (DBMS)",
        "Database Management Systems (DBMS)",
    ],
    ["https://www.udemy.com/topic/sql-server/", "SQL Server", "SQL Server"],
    ["https://www.udemy.com/topic/postgresql/", "PostgreSQL", "PostgreSQL"],
    ["https://www.udemy.com/topic/apache-kafka/", "Apache Kafka", "Apache Kafka"],
    ["https://www.udemy.com/topic/mongodb/", "MongoDB", "MongoDB"],
    [
        "https://www.udemy.com/topic/database-programming/",
        "Programação de banco de dados",
        "Database Programming",
    ],
    ["https://www.udemy.com/topic/oracle-sql/", "Oracle SQL", "Oracle SQL"],
    [
        "https://www.udemy.com/topic/selenium-webdriver/",
        "Selenium WebDriver",
        "Selenium WebDriver",
    ],
    [
        "https://www.udemy.com/topic/automation-testing/",
        "Testes de automação",
        "Automation Testing",
    ],
    ["https://www.udemy.com/topic/java/", "Java", "Java"],
    ["https://www.udemy.com/topic/postman/", "Postman", "Postman"],
    [
        "https://www.udemy.com/topic/selenium-testing-framework/",
        "Selenium Testing Framework",
        "Selenium Testing Framework",
    ],
    [
        "https://www.udemy.com/topic/istqb-certified-tester-foundation-level-ctfl/",
        "ISTQB Certified Tester Foundation Level (CTFL)",
        "ISTQB Certified Tester Foundation Level (CTFL)",
    ],
    ["https://www.udemy.com/topic/cypressio/", "Cypress.io", "Cypress.io"],
    [
        "https://www.udemy.com/topic/playwright/",
        "Microsoft Playwright",
        "Microsoft Playwright",
    ],
    [
        "https://www.udemy.com/topic/data-structures/",
        "Estruturas de dados",
        "Data Structures",
    ],
    ["https://www.udemy.com/topic/algorithms/", "Algoritmos", "Algorithms"],
    [
        "https://www.udemy.com/topic/coding-interview/",
        "Entrevista de programador",
        "Coding Interview",
    ],
    [
        "https://www.udemy.com/topic/certified-kubernetes-application-developer-ckad/",
        "Certified Kubernetes Application Developer (CKAD)",
        "Certified Kubernetes Application Developer (CKAD)",
    ],
    [
        "https://www.udemy.com/topic/software-architecture/",
        "Arquitetura de software",
        "Software Architecture",
    ],
    ["https://www.udemy.com/topic/microservices/", "Microsserviços", "Microservices"],
    [
        "https://www.udemy.com/topic/software-practices/",
        "Práticas de software",
        "Software Practices",
    ],
    [
        "https://www.udemy.com/topic/java-algorithms/",
        "Algoritmos em Java",
        "Java Algorithms",
    ],
    ["https://www.udemy.com/topic/elasticsearch/", "Elasticsearch", "Elasticsearch"],
    ["https://www.udemy.com/topic/docker/", "Docker", "Docker"],
    ["https://www.udemy.com/topic/git/", "Git", "Git"],
    ["https://www.udemy.com/topic/kubernetes/", "Kubernetes", "Kubernetes"],
    ["https://www.udemy.com/topic/jira/", "JIRA", "JIRA"],
    ["https://www.udemy.com/topic/github/", "GitHub", "GitHub"],
    ["https://www.udemy.com/topic/confluence/", "Confluence", "Confluence"],
    ["https://www.udemy.com/topic/terraform/", "Terraform", "Terraform"],
    [
        "https://www.udemy.com/topic/prompt-engineering/",
        "Engenharia de prompt",
        "Prompt Engineering",
    ],
    ["https://www.udemy.com/topic/devops/", "DevOps", "DevOps"],
    ["https://www.udemy.com/topic/wordpress/", "WordPress", "WordPress"],
    [
        "https://www.udemy.com/topic/microsoft-power-platform/",
        "Microsoft Power Platform",
        "Microsoft Power Platform",
    ],
    [
        "https://www.udemy.com/topic/bubble-visual-programming/",
        "Programação visual com o Bubble",
        "Visual Programming with Bubble",
    ],
    [
        "https://www.udemy.com/topic/microsoft-powerapps/",
        "Microsoft Power Apps",
        "Microsoft Power Apps",
    ],
    ["https://www.udemy.com/topic/web-design/", "Web design", "Web Design"],
    [
        "https://www.udemy.com/topic/artificial-intelligence/",
        "Inteligência artificial",
        "Artificial Intelligence",
    ],
    ["https://www.udemy.com/topic/elementor/", "Elementor", "Elementor"],
    ["https://www.udemy.com/topic/wix/", "Wix", "Wix"],
    [
        "https://www.udemy.com/topic/web-development/",
        "Desenvolvimento Web",
        "Web Development",
    ],
]

COURSE_ANCHORS_SELECTOR = 'a[href^="/course/"]'


def scrap_course_urls():
    logger.info("Gattering courses urls")
    random.shuffle(UDEMY_TOPICS)
    courses_urls = []

    t = UDEMY_TOPICS[0]

    logger.info(f"Scrapping topic '{t[2]}'...")

    wait_time = random.randint(3, 3 * 60)

    logger.info(f"Waiting {wait_time}s before topic load...")

    time.sleep(wait_time)

    driver = generate_driver()

    logger.info(f"Loading topic...")

    course_anchors = find_element_by_selector(
        driver,
        t[0],
        COURSE_ANCHORS_SELECTOR,
        single=False,
        screenshot=True,
        load_wait=8,
    )

    courses_urls_found = list(
        map(
            lambda el: el.get_attribute("href"),
            course_anchors,
        )
    )

    logger.info(f"Yielded {len(courses_urls_found)} courses!")

    courses_urls.extend(courses_urls)

    driver.quit()

    logger.info("Finished courses urls")

    return courses_urls
