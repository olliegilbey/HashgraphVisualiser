import java.nio.charset.StandardCharsets;

import com.swirlds.platform.Console;
import com.swirlds.platform.Event;
import com.swirlds.platform.Platform;
import com.swirlds.platform.SwirldMain;
import com.swirlds.platform.SwirldState;
import java.io.BufferedWriter;
import java.io.OutputStreamWriter;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * Creates a node which constantly sends out it's name with a counter.
 * TODO implement occasional dumps of the events for later processing
 */
public class HashgraphVisualizerSDKMain implements SwirldMain {
	/** the platform running this app */
	public Platform platform;
	/** ID number for this member */
	public long selfId;
	/** a console window for text output */
	public Console console;
	/** sleep this many milliseconds after each sync */
	public final int sleepPeriod = 100;
	// Socket connection for dumping data
	private BufferedWriter dataStream;

	@Override
	public void preEvent() {
	}

	@Override
	public void init(Platform platform, long id) {
		this.platform = platform;
		this.selfId = id;
		this.console = platform.createConsole(true); // create the window, make it visible
		platform.setAbout("Hello Swirld v. 1.0\n"); // set the browser's "about" box
		platform.setSleepAfterSync(sleepPeriod);
	}

	@Override
	public void run() {
		String myName = platform.getState().getAddressBookCopy()
				.getAddress(selfId).getSelfName(); // name of event creator
		int count = 0; // event counter
		String lastReceived = "";

		console.out.println("Hello Swirld from " + myName);

		platform.createTransaction(transaction);
		String lastReceived = "";

		// Alice dumps events to the socket
		if (myName == "Alice".getBytes()) {
			try {
				ServerSocket ss = new ServerSocket(54321);
				Socket conn = ss.accept();
				dataStream = new BufferedWriter(new OutputStreamWriter(conn.getOutputStream()));
			} catch (Exception e) {
			}
		}
		
		while (true) {

			// Create the transaction as a string of utf-8 characters consisting of
			// a node's name and the transaction counter
			byte[] transaction = (myName + count++).getBytes(StandardCharsets.UTF_8);
			// Send the transaction. The platform passes the transaction to our state
			// and to the local community. The community decides the order together
			platform.createTransaction(transaction);
			HashgraphState state = (HashgraphState) platform
					.getState();
			String received = state.getReceived();

			if (!lastReceived.equals(received)) {
				lastReceived = received;
				console.out.println("Received: " + received); // print all received transactions
			}
			
			if (myName == "Alice".getBytes()) {
				for (Event event: platform.getAllEvents()) {
					console.out.println("Sending event " + event);
					try {
						dataStream.append(event.toString());
					} catch (Exception e) {
					}
				}
				try {
					dataStream.flush();
				} catch (Exception e) {
				}
			}
			
			try {
				Thread.sleep(sleepPeriod);
			} catch (Exception e) {
			}
		}
	}

	@Override
	public SwirldState newState() {
		return new HashgraphState();
	}
}
