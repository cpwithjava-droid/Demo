@SpringBootApplication
@RestController
@RequestMapping("/api")
public class DemoApplication {

    private static final Logger logger = LoggerFactory.getLogger(DemoApplication.class);
    private static final String APP_VERSION = "1.0.0";

    // --- FAKE TOKEN FOR GITLEAKS TEST ---
    private static final String FAKE_API_TOKEN = "ghp_1234567890abcdefTESTTOKEN";

    public static void main(String[] args) {
        SpringApplication.run(DemoApplication.class, args);
    }

    @GetMapping("/hello")
    public String hello() {
        logger.info("GET /hello called");
        return "Hello from CI/CD pipeline!";
    }

    @GetMapping("/health")
    public String health() {
        logger.info("GET /health called");
        return "OK";
    }

    @GetMapping("/version")
    public String version() {
        logger.info("GET /version called");
        return "App version: " + APP_VERSION;
    }

    @PostMapping("/greet")
    public GreetingResponse greet(@RequestBody GreetingRequest request) {
        logger.info("POST /greet called with name: {}", request.getName());
        String message = "Hello, " + request.getName() + "! Welcome to the CI/CD pipeline demo.";
        return new GreetingResponse(message);
    }

    // DTO classes
    public static class GreetingRequest {
        private String name;

        public String getName() {
            return name;
        }

        public void setName(String name) {
            this.name = name;
        }
    }

    public static class GreetingResponse {
        private String message;

        public GreetingResponse(String message) {
            this.message = message;
        }

        public String getMessage() {
            return message;
        }

        public void setMessage(String message) {
            this.message = message;
        }
    }
}
