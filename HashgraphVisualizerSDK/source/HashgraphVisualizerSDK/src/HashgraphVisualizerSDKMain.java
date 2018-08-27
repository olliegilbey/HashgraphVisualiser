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
 * This HelloSwirld creates a single transaction, consisting of the string "Hello Swirld", and then goes
 * into a busy loop (checking once a second) to see when the state gets the transaction. When it does, it
 * prints it, too.
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
				.getAddress(selfId).getSelfName();

		console.out.println("Hello Swirld from " + myName);

		// create a transaction. For this example app,
		// we will define each transactions to simply
		// be a string in UTF-8 encoding.
		byte[] transaction = myName.getBytes(StandardCharsets.UTF_8);

		// Send the transaction to the Platform, which will then
		// forward it to the State object.
		// The Platform will also send the transaction to
		// all the other members of the community during syncs with them.
		// The community as a whole will decide the order of the transactions
		platform.createTransaction(transaction);
		String lastReceived = "";

		// Alice dumps events to the socket
		if (platform.getSwirldId() == "Alice".getBytes()) {
			try {
				ServerSocket ss = new ServerSocket(54321);
				Socket conn = ss.accept();
				dataStream = new BufferedWriter(new OutputStreamWriter(conn.getOutputStream()));
			} catch (Exception e) {
			}
		}
		
		while (true) {
			HashgraphState state = (HashgraphState) platform
					.getState();
			String received = state.getReceived();

			if (!lastReceived.equals(received)) {
				lastReceived = received;
				console.out.println("Received: " + received); // print all received transactions
			}
			
			if (platform.getSwirldId() == "Alice".getBytes()) {
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
