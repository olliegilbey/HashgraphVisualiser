package hashgraphvisualizersdk;

import com.swirlds.platform.Browser;
import com.swirlds.platform.Console;
import com.swirlds.platform.Event;
import com.swirlds.platform.Platform;
import com.swirlds.platform.SwirldMain;
import com.swirlds.platform.SwirldState;
import java.util.Arrays;

public class HashgraphVisualizerSDK implements SwirldMain {

	public static void main(String[] args) {
		System.out.println("in main");
		Browser.main(args);
	}
	
	private Platform platform;
	private long id;
	private Event[] events;
	private Console console;
	
	@Override
	public void init(Platform platform, long id) {
		this.platform = platform;
		this.id = id;
		this.console = platform.createConsole(true);
		console.out.println("app init");
	}

	@Override
	public void run() {
		console.out.println("app run");
		while (true) {
			events = platform.getAllEvents();
			console.out.println(Arrays.toString(events));
		}
	}

	@Override
	public void preEvent() {
	}

	@Override
	public SwirldState newState() {
		return new HashgraphState();
	}

}
