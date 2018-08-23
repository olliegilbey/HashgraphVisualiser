import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.swirlds.platform.Address;
import com.swirlds.platform.AddressBook;
import com.swirlds.platform.FCDataInputStream;
import com.swirlds.platform.FCDataOutputStream;
import com.swirlds.platform.FastCopyable;
import com.swirlds.platform.Platform;
import com.swirlds.platform.SwirldState;
import com.swirlds.platform.Utilities;

/**
 * This holds the current state of the swirld. For this simple "hello swirld" code, each transaction is just
 * a string, and the state is just a list of the strings in all the transactions handled so far, in the
 * order that they were handled.
 */
public class HashgraphState implements SwirldState {
	
	/**
	 * The shared state is just a list of the strings in all transactions, listed in the order received
	 * here, which will eventually be the consensus order of the community.
	 */
	private List<String> strings = new ArrayList<String>();
	/** names and addresses of all members */
	private AddressBook addressBook;

	/** @return all the strings received so far from the network */
	public synchronized List<String> getStrings() {
		return strings;
	}

	/** @return all the strings received so far from the network, concatenated into one */
	public synchronized String getReceived() {
		return strings.toString();
	}

	/** @return the same as getReceived, so it returns the entire shared state as a single string */
	public synchronized String toString() {
		return strings.toString();
	}
	
	@Override
	public synchronized AddressBook getAddressBookCopy() {
		return addressBook.copy();
	}

	@Override
	public synchronized FastCopyable copy() {
		HashgraphState copy = new HashgraphState();
		copy.copyFrom(this);
		return copy;
	}

	@Override
	public synchronized void copyTo(FCDataOutputStream outStream) {
		try {
			Utilities.writeStringArray(outStream,
					strings.toArray(new String[0]));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Override
	public synchronized void copyFrom(FCDataInputStream inStream) {
		try {
			strings = new ArrayList<String>(
					Arrays.asList(Utilities.readStringArray(inStream)));
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

	@Override
	public synchronized void copyFrom(SwirldState old) {
		strings = new ArrayList<String>(((HashgraphState) old).strings);
		addressBook = ((HashgraphState) old).addressBook.copy();
	}

	@Override
	public synchronized void handleTransaction(long id, boolean consensus,
			Instant timestamp, byte[] transaction, Address address) {
		strings.add(new String(transaction, StandardCharsets.UTF_8));
	}

	@Override
	public void noMoreTransactions() {
	}

	@Override
	public synchronized void init(Platform platform, AddressBook addressBook) {
		this.addressBook = addressBook;
	}
}
